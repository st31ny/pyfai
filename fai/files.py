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
from typing import Sequence
import pathlib

from . import env, subprocess

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


def chmod(path: TargetPath,
          *,
          mode: int = 0o644,
          user: str = 'root',
          group: str = 'root'):
    """Change mode and owner/group of a file

    :param path: path of file to chmod
    :param mode: desired file mode
    :param user: desired file owner
    :param group: desired file group
    :raises FileNotFoundError: if :any:`path <chmod.params.path>` does not exist

    This function is idempotent.
    """
    assert not user.startswith('-')
    assert not group.startswith('-')
    resolve(path).chmod(mode)
    # we need to run this in the target to resolve user names correctly
    subprocess.run(['chown', f'{user}:{group}', str(path)])


def mkdir(path: TargetPath,
          *,
          mode: int = 0o755,
          user: str = 'root',
          group: str = 'root'):
    """Create a directory relative to target

    :param path: path of directory to create
    :param mode: desired directory mode
    :param user: desired directory owner
    :param group: desired directory group
    :raise FileExistsError: if :any:`path <mkdir.params.path>` is a non-directory file

    Parent directories are created with default mode/owner/group if they do not
    exist.

    This function is idempotent.
    """
    resolve(path).mkdir(mode=mode, parents=True, exist_ok=True)
    chmod(path, mode=mode, user=user, group=group)


def fcopy(
    *args: Sequence[TargetPath],
    recursively: bool = False,
    user: str = 'root',
    group: str = 'root',
    mode: int = 0o644,
    remove_backup: bool = True,
    delete_orphan: bool = True,
    ignore_warnings: bool = True,
):
    """ Run `fcopy(8)`_

    :param args: paths of files to install
    :param recursively: enable recursive mode (``-r``)
    :param user: set file owner (``-m``)
    :param group: set file group (``-m``)
    :param mode: set file mode (``-m``)
    :param remove_backup: remove ``*.pre_fcopy`` backup files (``-B``)
    :param delete_orphan: delete target files when no class applies (``-d``)
    :param ignore_warnings: ignore warnings when no class applies (``-i``)

    .. _`fcopy(8)`: https://fai-project.org/doc/man/fcopy.html
    """
    arg_map = {
        '-B': remove_backup,
        '-d': delete_orphan,
        '-i': ignore_warnings,
        '-r': recursively,
    }
    the_mode = f'{user},{group},{mode:o}'
    fargs = ['fcopy', '-v', '-m', the_mode]
    for option_name, option_set in arg_map.items():
        if option_set:
            fargs.append(option_name)
    fargs.extend(str(p) for p in args)
    subprocess.run_installer(fargs)
