""" File Handling
    =============

    Pyfai strictly differentiates between virtual paths in the target system
    (:any:`TargetPath`) and physical paths in the installer system
    (:any:`InstallerPath`). While the former are always rooted in the target
    system's filesystem root, only the latter can be resolved as pyfai is
    running in the installer system.

    Most functions in this package work on :any:`TargetPath`\\ s. Sometimes,
    however, access to the actual target filesystem is required. Therefore
    this module provides functions to convert between both path types.

    During softupdate, the installer system actually IS the target system, so
    in this case the value of a :any:`TargetPath` to a specific file is
    identical to the :any:`InstallerPath` to the same file, although both are
    still separate classes.

    Since a :any:`TargetPath` is only virtual and not (at least not during an
    install) always resolvable it is an alias to :any:`pathlib.PurePosixPath`.
    Conversely, an :any:`InstallerPath` is actually simply a path in the
    currently running system, so it aliases :any:`pathlib.PosixPath`.

    To convert between :any:`TargetPath`\\ s and :any:`InstallerPath`\\ s, use
    :any:`resolve()` and :any:`unresolve()`.
"""
from __future__ import annotations
import pathlib

from . import env

InstallerPath: type = pathlib.PosixPath
"""Physical path in the installer system"""

_ip_root = InstallerPath('/')

TargetPath: type = pathlib.PurePosixPath
"""Virtual path in the target system"""

_tp_root = TargetPath('/')


def resolve(target_path: TargetPath) -> InstallerPath:
    """Resolve a path in the target system

    :param target_path: pure path in the target system
    :return: absolute path in the installer system within :any:`env.target`
    """
    if target_path.is_absolute():
        target_path = target_path.relative_to(_tp_root)
    result = env.target / target_path
    assert env.target in result.parents
    assert result.is_absolute()
    return result


def unresolve(installer_path: InstallerPath) -> TargetPath:
    """Find the target path for a resolved path

    :param installer_path: resolved path
    :return: absolute path in target system
    :raise ValueError: if :any:`installer_path` not within :any:`env.target`
    """
    result = _tp_root / installer_path.relative_to(env.target)
    assert result.is_absolute()
    return result
