# Sphinx Configuration
#
# doc: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import datetime
import pathlib
import pkg_resources
import sys
import toml

_rootdir = pathlib.Path(__file__).parents[1].absolute()
sys.path.append(str(_rootdir))
import fai


# -- Project information -----------------------------------------------------

project = "pyfai"
author = "{} contributors".format(project)
copyright_years = ", ".join(str(y) for y in range(2021, datetime.date.today().year + 1))
copyright = "{} {}".format(copyright_years, author)
release = fai.__version__ or pkg_resources.get_distribution('fai').version
version = release


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

#templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
#html_static_path = ['_static']
