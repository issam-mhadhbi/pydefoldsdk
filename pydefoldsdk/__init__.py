from .render import *
from .resource import *
from .ddf import *
from .engine import *
from .gamesys import *
from .gameobject import *
from .graphics import *
from .script import *
from .rig_ddf_pb2 import *
from .particle_ddf_pb2 import *
from .input_ddf_pb2 import *

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
