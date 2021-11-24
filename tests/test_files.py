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


@pytest.fixture
def resolve_patch(mocker):
    return mocker.patch('fai.files.resolve', autospec=True, spec_set=True)


@pytest.fixture
def subprocess_patch(mocker):
    return mocker.patch('fai.subprocess.run', autospec=True, spec_set=True)


def test_chmod_defaults(resolve_patch, subprocess_patch):
    p = files.TargetPath('/etc/fstab')
    files.chmod(p)

    resolve_patch.assert_called_once_with(p)
    resolve_patch.return_value.chmod.assert_called_once_with(0o644)
    subprocess_patch.assert_called_once_with(['chown', 'root:root', str(p)])


def test_chmod_overrides(resolve_patch, subprocess_patch):
    p = files.TargetPath('/usr/local/bin/myscript')
    files.chmod(p, user='root', group='staff', mode=0o755)

    resolve_patch.assert_called_once_with(p)
    resolve_patch.return_value.chmod.assert_called_once_with(0o755)
    subprocess_patch.assert_called_once_with(['chown', 'root:staff', str(p)])


@pytest.fixture
def chmod_patch(mocker):
    return mocker.patch('fai.files.chmod', autospec=True, spec_set=True)


def test_mkdir_defaults(resolve_patch, chmod_patch):
    p = files.TargetPath('/var/data')
    files.mkdir(p)

    resolve_patch.assert_called_once_with(p)
    resolve_patch.return_value.mkdir.assert_called_once_with(mode=0o755,
                                                             parents=True,
                                                             exist_ok=True)
    chmod_patch.assert_called_once_with(p,
                                        mode=0o755,
                                        user='root',
                                        group='root')


def test_mkdir_overrides(resolve_patch, chmod_patch):
    p = files.TargetPath('/var/secret')
    files.mkdir(p, user='admin', group='staff', mode=0o700)

    resolve_patch.assert_called_once_with(p)
    resolve_patch.return_value.mkdir.assert_called_once_with(mode=0o700,
                                                             parents=True,
                                                             exist_ok=True)
    chmod_patch.assert_called_once_with(p,
                                        mode=0o700,
                                        user='admin',
                                        group='staff')


@pytest.fixture
def subprocess_inst_patch(mocker):
    return mocker.patch('fai.subprocess.run_installer',
                        autospec=True,
                        spec_set=True)


def test_fcopy_defaults(subprocess_inst_patch):
    sip = subprocess_inst_patch

    p1 = files.TargetPath('/etc/network/interfaces')
    p2 = files.TargetPath('/etc/fai/fai.conf')
    files.fcopy(p1, p2)

    sip.assert_called_once()
    args = sip.call_args[0][0]
    assert args[0] == 'fcopy'
    assert args[-2:] == [str(p1), str(p2)]
    assert set(args[1:-2]) == \
            {'-v', '-i', '-B', '-d', '-m', 'root,root,644'}


def test_fcopy_recursive(subprocess_inst_patch):
    sip = subprocess_inst_patch

    p1 = files.TargetPath('/etc/apt')
    files.fcopy(p1,
                recursively=True,
                ignore_warnings=False,
                delete_orphan=False,
                mode=0o755,
                user='admin',
                group='staff',
                remove_backup=False)

    sip.assert_called_once()
    args = sip.call_args[0][0]
    assert args[0] == 'fcopy'
    assert args[-1:] == [str(p1)]
    assert set(args[1:-1]) == \
            {'-v', '-m', 'admin,staff,755', '-r'}
