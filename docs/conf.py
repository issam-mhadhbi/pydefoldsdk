import os
import sys

# Include root package
sys.path.insert(0, os.path.abspath('..'))

# Project info
project = 'pydefoldsdk'
author = 'Mhadhbi Issam'

# Read version safely
version_file = os.path.abspath(os.path.join('..', 'VERSION'))
if os.path.exists(version_file):
    release = open(version_file).read().strip()
else:
    release = '0.0.0'  # fallback if VERSION file missing

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',   # generate docs from docstrings
    'sphinx.ext.napoleon',  # support Google/NumPy docstrings
    'myst_parser',           # enable Markdown support
]

# Support Markdown files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']