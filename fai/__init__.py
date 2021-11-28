""" FAI Package Root Module
    =======================

    The root module provides access to most basic FAI functions
    and environment variables.

    The following elements from other modules are re-exported:

    * :any:`fai.env.* <fai.env>`
    * :any:`fai.subprocess.run`
    * :any:`fai.subprocess.run_installer`
    * :any:`fai.files.InstallerPath`
    * :any:`fai.files.TargetPath`
    * :any:`fai.files.resolve`
    * :any:`fai.files.unresolve`
    * :any:`fai.files.fcopy`
"""

__version__ = None
""" Package version
"""

try:
    from ._version import version as __version__
except ImportError:
    pass

# pylint: disable=wrong-import-position
from .env import *
from .subprocess import run, run_installer
from .files import InstallerPath, TargetPath, resolve, unresolve, fcopy
