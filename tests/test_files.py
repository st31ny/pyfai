import pytest

import pathlib

from fai import files, env


@pytest.fixture
def faienv(monkeypatch):
    monkeypatch.setattr(env, 'target', pathlib.PosixPath('/target'))


def test_resolve_relative(faienv):
    tp = files.TargetPath('etc/fai/fai.conf')
    ip = files.resolve(tp)
    assert ip == pathlib.PosixPath('/target/etc/fai/fai.conf')
    assert isinstance(ip, pathlib.PosixPath)


def test_resolve_absolute(faienv):
    tp = files.TargetPath('/etc/fai/fai.conf')
    ip = files.resolve(tp)
    assert ip == pathlib.PosixPath('/target/etc/fai/fai.conf')
    assert isinstance(ip, pathlib.PosixPath)


def test_unresolve_path_in_target(faienv):
    ip = files.InstallerPath('/target/etc/fai/fai.conf')
    tp = files.unresolve(ip)
    assert tp == pathlib.PurePosixPath('/etc/fai/fai.conf')
    assert isinstance(tp, pathlib.PurePosixPath)


def test_unresolve_path_outside_target(faienv):
    ip = files.InstallerPath('/etc/fai/fai.conf')
    with pytest.raises(ValueError):
        files.unresolve(ip)
