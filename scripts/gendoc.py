import sys 
import os  , subprocess
from pathlib import Path
class Utils : 
	def get_git_root(path: Path = Path.cwd()) -> Path:
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
sys.path.append(str(Path(Utils.get_git_root())))
from pydefoldsdk import sdk
from google.protobuf.descriptor import FieldDescriptor
import os



class SdkGenDoc:
    PROTOBUF_TYPE_TO_PYTHON_TYPE = {
        FieldDescriptor.TYPE_DOUBLE: 'float',
        FieldDescriptor.TYPE_FLOAT: 'float',
        FieldDescriptor.TYPE_INT64: 'int',
        FieldDescriptor.TYPE_UINT64: 'int',
        FieldDescriptor.TYPE_INT32: 'int',
        FieldDescriptor.TYPE_FIXED64: 'int',
        FieldDescriptor.TYPE_FIXED32: 'int',
        FieldDescriptor.TYPE_BOOL: 'bool',
        FieldDescriptor.TYPE_STRING: 'str',
        FieldDescriptor.TYPE_BYTES: 'bytes',
        FieldDescriptor.TYPE_UINT32: 'int',
        FieldDescriptor.TYPE_ENUM: 'int',
        FieldDescriptor.TYPE_SFIXED32: 'int',
        FieldDescriptor.TYPE_SFIXED64: 'int',
        FieldDescriptor.TYPE_SINT32: 'int',
        FieldDescriptor.TYPE_SINT64: 'int',
    }

    @staticmethod
    def get_type_enums(typ):
        enums = {}
        for enum_name, enum_type in typ.DESCRIPTOR.enum_types_by_name.items():
            enums[enum_name] = [f"{key} = {value.number}" for key, value in enum_type.values_by_name.items()]
        return enums

    @staticmethod
    def parse_field(typ, field, name):
        # Determine if this is a repeated field
        repeated = getattr(field, "label", None) == FieldDescriptor.LABEL_REPEATED

        if field.type == FieldDescriptor.TYPE_MESSAGE:
            field_type = field.message_type._concrete_class.__name__
            if repeated:
                field_type = f"List[{field_type}]"
        else:
            field_type = SdkGenDoc.PROTOBUF_TYPE_TO_PYTHON_TYPE.get(field.type)
            if repeated:
                field_type = f"List[{field_type}]"

        return {"name": name, "type": field_type}

    @staticmethod
    def parse_fields(typ):
        fields = {}
        for name, field in typ.DESCRIPTOR.fields_by_name.items():
            fields[name] = SdkGenDoc.parse_field(typ=typ, field=field, name=name)
        return fields

    @staticmethod
    def parse_type(typ):
        return {"enums": SdkGenDoc.get_type_enums(typ), "fields": SdkGenDoc.parse_fields(typ)}

    def gen_doc(self, docs_folder="docs"):
        os.makedirs(docs_folder, exist_ok=True)

        for typ_name, typ in sdk._asdict().items():
            info = SdkGenDoc.parse_type(typ)
            lines = [f"# Message: `{typ_name}`\n"]

            if info["fields"]:
                lines.append("### Fields:")
                for fname, fdata in info["fields"].items():
                    lines.append(f"- **{fname}**: `{fdata['type']}`")
            else:
                lines.append("_No fields_\n")

            if info["enums"]:
                lines.append("\n### Enums:")
                for enum_name, values in info["enums"].items():
                    lines.append(f"- **{enum_name}**:")
                    for v in values:
                        lines.append(f"  - `{v}`")

            lines.append("\n---\n")

            # Write a separate markdown file per message
            mdfile = os.path.join(docs_folder, f"{typ_name}.md")
            with open(mdfile, "w") as f:
                f.write("\n".join(lines))
            print(f"Generated {mdfile}")


if __name__ == "__main__":
    SdkGenDoc().gen_doc()

