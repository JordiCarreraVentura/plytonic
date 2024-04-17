import os
import subprocess
import sys

from logger import LOGGER
from __init__ import PLYTONIC_FOLDER, self_install


if __name__ == '__main__':

    path_env = os.path.join(PLYTONIC_FOLDER, 'bin')
    python_env = f'{path_env}/python'

    if not os.path.exists(path_env):
        LOGGER('Virtual environment does not seem to exist yet. Will install '
               'necessary dependencies.')
        self_install()

    if sys.executable != python_env:
        subprocess.Popen([
            python_env, __file__
        ] + sys.argv[1:])

    else:
        from user_interface import UserInterfaceLauncher
        from example_data import make_example

        make_example()

        ui = UserInterfaceLauncher()
        ui()