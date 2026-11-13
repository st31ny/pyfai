"""" ToDo
    =============

    This module provides some functions to work with system services e.g. creating 
    system user or units
"""
from . import env, files, subprocess


def create_system_user(username, *, group=None, home=None, shell='/bin/false'):
    """ @brief  Create a system user if it does not exist
        @param  username Username of the new user
        @param  group Primary group of user. If None, group 'nogroup' is assigned.
        @param  home Optional home directory to create. If None, set home to '/nonexistent'
                    and do not create it.
        @param  The user's shell.

        If the user exists, set the shell and home directory correctly.
    """
    nonexistent = '/nonexistent'
    assert not username.startswith('-')
    assert not shell.startswith('-')
    # create group
    if group:
        assert not group.startswith('-')
        # addgroup fails silently if group exists
        args = ['addgroup', '--quiet', '--system', group]
        subprocess.run(args)
    else:
        group = 'nogroup'
    # create user (adduser fails silently if user already exists)
    args = ['adduser', '--quiet', '--system']
    if home:
        assert not str(home).startswith('-')
        args.extend(['--home', home])
    else:
        args.extend(['--no-create-home', '--home', nonexistent])
    args.append(username)
    subprocess.run(args)
    # set shell, homedir, and group
    args = ['usermod', '--shell', shell, '-g', group]
    if home:
        args.extend(['--move-home', '--home', home])
    else:
        args.extend(['--home', nonexistent])
    args.append(username)
    subprocess.run(args)
    # ensure home dir exists
    if home:
        files.mkdir(home, user=username, group=group)


def systemd_install(unit, *, start=None):
    """ @brief  Install and enable a systemd unit
        @param  unit Name of the systemd unit (including the service type suffix)
        @param  start If True, start the systemd unit if possible (i.e., if softupdate
                    is running). If None, start unit if it is enabled.

        The file /etc/systemd/system/<unit> and files in /etc/systemd/system/<unit>.d/
        are fcopy'd. Non-existing files do not cause failure.

        After installation, the unit is 'preset', i.e. enabled iff it has an install
        section.

        Finally, in softupdate, the unit is started iff start==True or start==None and
        the unit is enabled.
    """
    assert '/' not in unit
    assert not unit.startswith('-')
    # install unit files
    files.fcopy(f'etc/systemd/system/{unit}')
    files.fcopy(f'etc/systemd/system/{unit}.d/', recursively=True)
    # enable/start service
    subprocess.run(['systemctl', 'preset', unit])
    if env.is_online():
        # if we are online, try to start the unit
        if start is None:
            # find out if the unit is enabled
            result = subprocess.run(['systemctl', 'is-enabled', unit],
                                    check=False)
            if result.returncode == 0 and result.stdout.startswith('enabled'):
                start = True
        if start:
            # we want to start the unit now
            subprocess.run(['systemctl', 'start', unit])
