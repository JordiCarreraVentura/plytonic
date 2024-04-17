import os
import platform
import subprocess
from enum import Enum


class OperativeSystem(Enum):
    Linux = 0
    Mac = 1
    Win = 2


class UnsupportedPlatformError(EnvironmentError):
    def __init__(self, *args, **kwargs):
        return



if platform.system() == 'Darwin':
    PLATFORM = OperativeSystem.Mac
elif platform.system() == 'Windows':
    PLATFORM = OperativeSystem.Win
else:
    PLATFORM = OperativeSystem.Linux


if PLATFORM is OperativeSystem.Win:
    raise UnsupportedPlatformError(OperativeSystem.Win.name)

SOURCE_FOLDER = os.getcwd()

path = os.path.realpath(__file__)
PLYTONIC_FOLDER = os.path.dirname(path)


def self_install():
    os.chdir(PLYTONIC_FOLDER)

    # Activate the virtual environment
    mk_env  = ' '.join(['virtualenv', '-p', 'python3.11', '.', ';'])
    act_env = 'source bin/activate ;'
    env_ins = ' '.join(['python', '-m', 'pip', 'install', '-r', 'requirements.txt', ';'])
    #dea_env = 'deactivate ;'
    dea_env = ''

    command = f'{mk_env}{act_env}{env_ins}{dea_env}'
    os.system(command)

    os.chdir(SOURCE_FOLDER)