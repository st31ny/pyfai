""" FAI Environment Variables
    =========================

    This module provides access to the most important `FAI environment
    variables`_. If not running from FAI, most variables here are
    :any:`None`.

    .. _`FAI environment variables`: https://wiki.fai-project.org/index.php/Variables

    .. hint::
        Many functions in the :py:mod:`fai` package depend on correct
        environment settings defined here. If you want to run your scripts
        without a full FAI process, make sure to define them properly.
"""
from typing import Mapping, Optional, Sequence, Union
import enum
import os
import pathlib
import shlex
import sys
import warnings

# pylint: disable-next=invalid-name; naming like FAI env var
classes: Sequence[str] = []
"""FAI classes (``$classes``)

:meta hide-value:
"""

CONFIG_SPACE: pathlib.Path = None
"""FAI config space (``$FAI``)

:meta hide-value:
"""

# pylint: disable-next=invalid-name; naming like FAI env var
target: pathlib.Path = None
"""FAI Installation target (``$target``)

:meta hide-value:
"""

ROOTCMD: Sequence[str] = []
"""Chroot command (``$ROOTCMD``)

The value from the environment is splitted with :any:`shlex.split` and can
thus be directly fed to :any:`subprocess.run`.

:meta hide-value:
"""


def is_online() -> bool:
    """Check if system installed/updated by FAI is online

    Some tasks such as starting a service are only possible when FAI is run
    within the target system (i.e. FAI is doing a softupdate).
    """
    return target is not None and target == pathlib.Path('/')


class Action(enum.Enum):
    """ Enum of well-known FAI actions """

    def _generate_next_value_(name, start, count, last_values):
        # pylint: disable=no-self-argument; done as offically documented
        return name

    # pylint: disable=invalid-name; naming like FAI actions

    sysinfo = enum.auto()  #: :meta hide-value:
    inventory = enum.auto()  #: :meta hide-value:
    install = enum.auto()  #: :meta hide-value:
    dirinstall = enum.auto()  #: :meta hide-value:
    softupdate = enum.auto()  #: :meta hide-value:


ACTION: Union[Action, str] = None
"""FAI action (``$FAI_ACTION``)

Well-known actions are mapped to elements of :any:`Action`. If running a custom
action, this is simply a :any:`str`.

:meta hide-value:
"""

LOGDIR: pathlib.Path = None
"""FAI log directory (``$LOGDIR``)

:meta hide-value:
"""


def _load_env(env: Mapping = os.environ):  # pylint: disable=dangerous-default-value

    def read_path(varname: str) -> Optional[pathlib.Path]:
        value = env.get(varname)
        if value is not None:
            return pathlib.Path(value)
        return None

    # pylint: disable=global-statement; we need to update the global vars here

    global classes  # pylint: disable=invalid-name; naming like FAI env var
    classes = str(env.get('classes', '')).split()

    global CONFIG_SPACE
    CONFIG_SPACE = read_path('FAI')

    global target  # pylint: disable=invalid-name; naming like FAI env var
    target = read_path('target')

    global ROOTCMD
    ROOTCMD = shlex.split(env.get('ROOTCMD', ''))

    global ACTION
    ACTION = env.get('FAI_ACTION')
    if ACTION is not None and hasattr(Action, ACTION):
        ACTION = Action[ACTION]

    global LOGDIR
    LOGDIR = read_path('LOGDIR')

    if not all([
            CONFIG_SPACE,
            target,
            #ROOTCMD, # $ROOTCMD can be empty
            ACTION,
            LOGDIR,
    ]) and 'sphinx' not in sys.modules and 'pytest' not in sys.modules:
        warnings.warn((
            "FAI environment variables not defined: Are you running in FAI? "
            "For testing, set $FAI, $target, $ROOTCMD, $FAI_ACTION, and $LOGDIR."
        ))


_load_env()
