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

    username = 'foo'
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


def test_create_user_options(faienv, subprocess_patch, files_mkdir_patch):
    sub = subprocess_patch
    dir = files_mkdir_patch

    username = 'foo'
    group = 'bar'
    home_dir = f'/home/{username}'
    shell = '/bin/bash'
    system.create_system_user(username,
                              group=group,
                              home=home_dir,
                              shell=shell)

    addgroup_args = ['addgroup', '--quiet', '--system', group]
    adduser_args = [
        'adduser', '--quiet', '--system', '--home', home_dir, username
    ]
    usermod_args = [
        'usermod', '--shell', shell, '-g', group, '--move-home', '--home',
        home_dir, username
    ]

    sub.assert_has_calls(
        [call(addgroup_args),
         call(adduser_args),
         call(usermod_args)])
    dir.assert_called_once_with(home_dir, user=username, group=group)


def test_create_user_fail(faienv, subprocess_patch, files_mkdir_patch):
    sub = subprocess_patch
    dir = files_mkdir_patch

    username = '-foo'

    with pytest.raises(AssertionError):
        system.create_system_user(username)

    sub.assert_not_called()
    dir.assert_not_called()


@pytest.fixture
def files_fcopy_patch(mocker):
    return mocker.patch("fai.files.fcopy", autospec=True, spec_set=True)


@pytest.fixture
def env_online_patch(mocker):
    return mocker.patch("fai.env.is_online", autospec=True, spec_set=True)


def test_systemd_install_default_online(faienv, files_fcopy_patch,
                                        subprocess_patch, env_online_patch):
    fcp = files_fcopy_patch
    sub = subprocess_patch

    unit = "testservice"
    env_online_patch.return_value = True
    sub.return_value.returncode = 0
    sub.return_value.stdout = 'enabled'

    system.systemd_install(unit)

    fcp.assert_has_calls([
        call(f'etc/systemd/system/{unit}'),
        call(f'etc/systemd/system/{unit}.d/', recursively=True)
    ])
    sub.assert_has_calls([
        call(['systemctl', 'preset', unit]),
        call(['systemctl', 'is-enabled', unit], check=False),
        call(['systemctl', 'start', unit])
    ])


def test_systemd_install_default_offline(faienv, files_fcopy_patch,
                                         subprocess_patch, env_online_patch):
    fcp = files_fcopy_patch
    sub = subprocess_patch

    unit = "testservice"
    env_online_patch.return_value = False

    system.systemd_install(unit)

    fcp.assert_has_calls([
        call(f'etc/systemd/system/{unit}'),
        call(f'etc/systemd/system/{unit}.d/', recursively=True)
    ])
    sub.assert_called_once_with(['systemctl', 'preset', unit])


def test_systemd_install_start(faienv, files_fcopy_patch, subprocess_patch,
                               env_online_patch):
    fcp = files_fcopy_patch
    sub = subprocess_patch

    unit = "testservice"
    env_online_patch.return_value = True

    system.systemd_install(unit, start=True)

    fcp.assert_has_calls([
        call(f'etc/systemd/system/{unit}'),
        call(f'etc/systemd/system/{unit}.d/', recursively=True)
    ])
    sub.assert_has_calls([
        call(['systemctl', 'preset', unit]),
        call(['systemctl', 'start', unit])
    ])


def test_systemd_install_fail(faienv, files_fcopy_patch, subprocess_patch,
                              env_online_patch):
    fcp = files_fcopy_patch
    sub = subprocess_patch

    unit = "-testservice"

    with pytest.raises(AssertionError):
        system.systemd_install(unit)

    fcp.assert_not_called()
    sub.assert_not_called()
