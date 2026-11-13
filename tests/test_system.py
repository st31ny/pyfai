import pytest
from unittest.mock import call

import pathlib

from fai import system, env


@pytest.fixture
def faienv(monkeypatch):
    monkeypatch.setattr(env, 'target', pathlib.PosixPath('/target'))


@pytest.fixture
def subprocess_patch(mocker):
    return mocker.patch('fai.subprocess.run', autospec=True, spec_set=True)


@pytest.fixture
def files_mkdir_patch(mocker):
    return mocker.patch('fai.files.mkdir', autospec=True, spec_set=True)


def test_create_user_default(faienv, subprocess_patch, files_mkdir_patch):
    sub = subprocess_patch
    dir = files_mkdir_patch

    username = 'Foo'
    system.create_system_user(username)

    adduser_args = [
        'adduser', '--quiet', '--system', '--no-create-home', '--home',
        '/nonexistent', username
    ]
    usermod_args = [
        'usermod', '--shell', '/bin/false', '-g', 'nogroup', '--home',
        '/nonexistent', username
    ]
    sub.assert_has_calls([call(adduser_args), call(usermod_args)])
    dir.assert_not_called()
