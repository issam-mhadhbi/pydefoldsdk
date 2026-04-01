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
    release = '0.0.0'

version = release

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
]

# Support both .rst and .md files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']