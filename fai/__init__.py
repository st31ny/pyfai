""" FAI Package Root Module
    =======================

    The root module provides access to most basic FAI functions
    and environment variables.
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

__all__ = ['CONFIG_SPACE', 'target', 'Action', 'ACTION']
