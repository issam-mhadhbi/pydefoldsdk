from pathlib import Path
import urllib.request, os, glob, sys, ast, stat, platform, subprocess, zipfile, shutil, importlib, collections

extra_code__ = """
import importlib, pkgutil, collections, os
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.text_format import Parse, MessageToString
from google.protobuf.json_format import MessageToDict, MessageToJson, ParseDict
from google.protobuf.message import Message

class TypesGenerator:
	def getDefoldTypes(self):
		result = {}

		pkg = importlib.import_module("pydefoldsdk")

		# Walk all submodules
		for _, modname, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
			try:
				module = importlib.import_module(modname)
			except Exception:
				continue  # skip broken modules

			for attr_name in dir(module):
				obj = getattr(module, attr_name)

				# Detect protobuf message classes
				if isinstance(obj, type) and issubclass(obj, Message):
					result[obj.__name__] = obj

		return collections.namedtuple("defoldsdk", result.keys())(**result)

sdk = TypesGenerator().getDefoldTypes()
__all__ = ["sdk"]
"""

class LocalImportFixer(ast.NodeTransformer):
	def __init__(self, pydefold_folder: Path):
		self.pydefold_folder = pydefold_folder.name
		excluded_folders = ['proto', 'google']
		self.interest_folders = [
			f.name for f in pydefold_folder.iterdir() if f.is_dir() and f.name not in excluded_folders
		]

	def visit_ImportFrom(self, node):
		if node.module and node.module in self.interest_folders:
			node.module = f"{self.pydefold_folder}.{node.module}"
		return node

	def visit_Import(self, node):
		for alias in node.names:
			if Path(alias.name.replace('.', '/')).exists():
				alias.name = f"{self.pydefold_folder}.{alias.name}"
		return node

class Settings:
	version = open("VERSION").read().strip()

class Build:
	def __init__(self):
		root = Path(self.get_git_root()) / ".build"
		os.makedirs(root , exist_ok=True)
		self.build_folder = root / f"pydefold-{Settings.version}"
		self.extract_dir = self.build_folder / f"defoldsdk-{Settings.version}"
		self.package_root = self.build_folder / "pydefoldsdk"
		self.setup()
		self.download_defoldsdk()
		self.build_proto_files()
		self.buildPackage()
		self.cleanModule()
		self.fix_inner_imports()
		self.test()

	def get_git_root(self,path: Path = Path.cwd()) -> Path:
		"""Return the root folder of the git repository, or None if not in a repo."""
		try:
			root = subprocess.check_output(
				["git", "rev-parse", "--show-toplevel"],
				cwd=path,
				stderr=subprocess.DEVNULL,
				text=True
			).strip()
			return Path(root)
		except subprocess.CalledProcessError:
			return None
	def setup(self):
		if self.build_folder.exists():
			if self.build_folder.is_dir():
				shutil.rmtree(self.build_folder)
			else:
				self.build_folder.unlink()
		self.build_folder.mkdir(parents=True, exist_ok=True)

	def download_defoldsdk(self):
		url = f"https://github.com/defold/defold/releases/download/{Settings.version}/defoldsdk.zip"
		print(url)
		zip_path = self.build_folder / "defoldsdk.zip"
		if self.extract_dir.exists():
			shutil.rmtree(self.extract_dir)
		self.extract_dir.mkdir(parents=True)
		urllib.request.urlretrieve(url, zip_path)
		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(self.extract_dir)
		zip_path.unlink()

	def build_proto_files(self):
		protoc = self.extract_dir / "defoldsdk" / "ext" / "bin" / f"{platform.machine()}-{platform.system().lower()}/protoc"
		protoc.chmod(protoc.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

		proto_folder = self.extract_dir / "defoldsdk" / "share" / "proto"
		python_out = self.build_folder
		include_google = self.extract_dir / "defoldsdk" / "ext" / "include"

		proto_files = list(proto_folder.rglob("*.proto")) + list(include_google.rglob("*.proto"))

		cmd = [
			str(protoc),
			"-I", str(proto_folder),
			"-I", str(include_google),
			f"--python_out={python_out}"
		] + [str(p) for p in proto_files]

		print("Running:", " ".join(cmd))
		subprocess.run(cmd, check=True)

		# Move folder up one level (grandparent)
		folder = self.extract_dir
		destination = folder.parent.parent / folder.name
		shutil.move(str(folder), str(destination))

	def buildPackage(self):
		dest = self.build_folder / "pydefoldsdk"
		self.package_root = dest
		dest.mkdir(parents=True, exist_ok=True)

		for item in self.build_folder.iterdir():
			if item == dest:
				continue
			shutil.move(str(item), str(dest))
		shutil.rmtree(dest / "google") 

	def cleanModule(self):
		root = self.package_root
		subfolders = [Path(dp) / d for dp, dn, fn in os.walk(root) for d in dn
					  if not (d.startswith("__") and d.endswith("__"))]

		for subfolder in subfolders:
			pb2_files = list(subfolder.glob("*_pb2.py"))
			# write __init__.py with relative imports
			with open(subfolder / "__init__.py", "w") as f:
				for f_pb2 in pb2_files:
					f.write(f"from .{f_pb2.stem} import *\n")

			# fix inner imports with AST
			for pb2_file in pb2_files:
				tree = ast.parse(pb2_file.read_text())
				fixer = LocalImportFixer(root)
				modified = fixer.visit(tree)
				pb2_file.write_text(ast.unparse(modified))

		# top-level __init__.py
		all_submodules = [f.name for f in subfolders] + [f.stem for f in root.glob("*_pb2.py")]
		with open(root / "__init__.py", "w") as f:
			for submodule in all_submodules:
				f.write(f"from .{submodule} import *\n")
			f.write(extra_code__)

	def fix_inner_imports(self):
		root_init = self.package_root / "__init__.py"
		for py_file in self.package_root.rglob("*.py"):
			if py_file == root_init:
				continue  # skip root __init__.py
			tree = ast.parse(py_file.read_text())
			fixer = LocalImportFixer(self.package_root)
			modified = fixer.visit(tree)
			py_file.write_text(ast.unparse(modified))

	def test(self):
		sys.path.append(str(self.package_root.parent))
		import pydefoldsdk
		from pydefoldsdk import sdk 
		print("pydefoldsdk imported:", pydefoldsdk)
		from google.protobuf.json_format import MessageToJson
		from google.protobuf.text_format import MessageToString, Parse
		print(sdk)

		content = '''
		name: "menu"
		scale_along_z: 0
		embedded_instances {
		  id: "go"
		  data: "components {\\n"
		  "  id: \\"menu\\"\\n"
		  "  component: \\"/examples/collection/proxy/menu.gui\\"\\n"
		  "  position {\\n"
		  "    x: 0.0\\n"
		  "    y: 0.0\\n"
		  "    z: 0.0\\n"
		  "  }\\n"
		  "  rotation {\\n"
		  "    x: 0.0\\n"
		  "    y: 0.0\\n"
		  "    z: 0.0\\n"
		  "    w: 1.0\\n"
		  "  }\\n"
		  "}\\n"
		  ""
		  position {
			x: 0.0
			y: 0.0
			z: 0.0
		  }
		  rotation {
			x: 0.0
			y: 0.0
			z: 0.0
			w: 1.0
		  }
		  scale3 {
			x: 1.0
			y: 1.0
			z: 1.0
		  }
		}
		'''


		collection = sdk.CollectionDesc()
		Parse(content.encode('utf-8'), collection)
		print(MessageToString(collection))
		print(MessageToJson(collection,preserving_proto_field_name=True))

# Run
if __name__ == '__main__':
	Build()


