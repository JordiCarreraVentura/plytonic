from user_interface import UserInterfaceLauncher
import os

from __init__ import self_install
from example_data import make_example
from logger import LOGGER


make_example()


if __name__ == '__main__':

    if not os.path.exists('bin'):
        LOGGER('Virtual environment does not seem to exist yet. Will install '
               'necessary dependencies.')
        self_install()

    ui = UserInterfaceLauncher()
    print(os.environ)
    ui()
    print(os.environ)