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
        args.extend(['--home', files.TargetPath(home)])
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
