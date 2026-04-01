import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # include root package

project = 'pydefoldsdk'
author = 'Mhadhbi Issam'
release = open("VERSION").read()

extensions = [
    'sphinx.ext.autodoc',   # generate docs from docstrings
    'sphinx.ext.napoleon',  # support Google/NumPy docstrings
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'  # Read the Docs theme
html_static_path = ['_static']