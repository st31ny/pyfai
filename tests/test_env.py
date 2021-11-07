import pytest

import pathlib

from fai import env


@pytest.fixture
def faienv_default(monkeypatch):
    monkeypatch.setenv('classes',
                       'DEFAULT\nLINUX  DEBIAN    GRUB\nhost   LAST')
    monkeypatch.setenv('FAI', '/var/lib/fai/config')
    monkeypatch.setenv('target', '/target')
    monkeypatch.setenv('ROOTCMD', 'chroot /target')
    monkeypatch.setenv('FAI_ACTION', 'install')


@pytest.fixture
def faienv_custom_action(faienv_default, monkeypatch):
    monkeypatch.setenv('FAI_ACTION', 'confupdate')


def test_all_empty():
    env._load_env()
    assert env.classes == []
    assert env.CONFIG_SPACE is None
    assert env.target is None
    assert env.ROOTCMD == []
    assert env.ACTION is None


def test_standard_conf(faienv_default):
    env._load_env()
    assert env.classes == [
        'DEFAULT', 'LINUX', 'DEBIAN', 'GRUB', 'host', 'LAST'
    ]
    assert env.CONFIG_SPACE == pathlib.Path('/var/lib/fai/config')
    assert env.target == pathlib.Path('/target')
    assert env.ROOTCMD == ['chroot', '/target']
    assert env.ACTION == env.Action.install


def test_custom_action(faienv_custom_action):
    env._load_env()
    assert env.ACTION == 'confupdate'
    assert env.ACTION != env.Action.softupdate
