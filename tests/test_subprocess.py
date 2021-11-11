import pytest

import pathlib
import subprocess

from fai import env, subprocess as sp


@pytest.fixture
def faienv(monkeypatch):
    monkeypatch.setattr(env, 'target', pathlib.PosixPath('/target'))
    monkeypatch.setattr(env, 'ROOTCMD', ['chroot', '/target'])


@pytest.fixture
def subprocess_patch(mocker):
    return mocker.patch('subprocess.run', autospec=True, spec_set=True)


def test_installer_defaults(faienv, subprocess_patch):
    mock_return = object()
    subprocess_patch.return_value = mock_return
    cmd = ['lsblk', '-O', '--json', '--sysroot', str(env.target)]
    result = sp.run_installer(cmd)
    assert result is mock_return
    subprocess_patch.assert_called_once_with(
        cmd,
        check=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
    )


def test_installer_overrides(faienv, subprocess_patch):
    mock_return = object()
    subprocess_patch.return_value = mock_return
    cmd = ['lsblk', '-O', '--json', '--sysroot', str(env.target)]
    result = sp.run_installer(cmd, check=False, stderr=subprocess.PIPE)
    assert result is mock_return
    subprocess_patch.assert_called_once_with(
        cmd,
        check=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_target_defaults(faienv, subprocess_patch):
    mock_return = object()
    subprocess_patch.return_value = mock_return
    cmd = ['getent', 'group', 'audio']
    result = sp.run(cmd)
    assert result is mock_return
    subprocess_patch.assert_called_once_with(
        ['chroot', '/target'] + cmd,
        check=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
    )


def test_target_overrides(faienv, subprocess_patch):
    mock_return = object()
    subprocess_patch.return_value = mock_return
    cmd = ['getent', 'group', 'audio']
    result = sp.run(cmd, check=False, stderr=subprocess.PIPE)
    assert result is mock_return
    subprocess_patch.assert_called_once_with(
        ['chroot', '/target'] + cmd,
        check=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
