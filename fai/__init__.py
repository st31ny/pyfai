""" FAI Package Root Module
    =======================

    The root module provides access to most basic FAI functions
    and environment variables.
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = None
