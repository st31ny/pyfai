""" Subprocesses
    ============

    This module provides a simple wrapper around :any:`python:subprocess.run`
    to run commands in the installer or in the target system.
"""
from typing import Sequence
import subprocess

from . import env


def run_installer(args: Sequence[str],
                  **kwargs) -> subprocess.CompletedProcess:
    """ Run command in installer system

    :param args: command and its arguments
    :param kwargs: additional arguments for :any:`python:subprocess.run`
    :return: process result
    :raise subprocess.CalledProcessError: when command is ``check``\\ ed and
        exits with error

    By default, commands are ``check``\\ ed (i.e., ``raise`` when exiting with
    error) and ``stdout`` is captured in ``text`` mode.

    Example::

        r = run_installer(['lsblk', '--json', '-O'])
        lsblk = json.loads(r.stdout)

    Example with :any:`kwargs <fai.subprocess.run_installer.params.kwargs>`::

        r = run_installer(['systemd-detect-virt'], check=False)
        is_virt = r.returncode == 0
    """
    kwargs.setdefault('check', True)
    kwargs.setdefault('universal_newlines', True)
    kwargs.setdefault('stdout', subprocess.PIPE)
    # pylint: disable=subprocess-run-check; check is always set in kwargs
    return subprocess.run(args, **kwargs)


def run(args: Sequence[str], **kwargs) -> subprocess.CompletedProcess:
    """ Run command in target system

    :param args: command and its arguments
    :param kwargs: additional arguments for :any:`python:subprocess.run`
    :return: process result
    :raise subprocess.CalledProcessError: when command is ``check``\\ ed and
        exits with error

    The command in :any:`args <fai.subprocess.run.params.args>` is prefixed with :any:`env.ROOTCMD`.

    Behaves like :any:`run_installer` otherwise.

    Example::

        r = run(['getent', 'group', 'audio'])
        audio_group_members = r.stdout.split(':')[3].split(',')
    """
    if env.ROOTCMD:
        args = env.ROOTCMD + args
    return run_installer(args, **kwargs)
