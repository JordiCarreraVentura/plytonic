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


def self_install():
    source_folder = os.getcwd()
    path = os.path.realpath(__file__)
    folder = os.path.dirname(path)
    os.chdir(folder)

    # Activate the virtual environment
    subprocess.run(['virtualenv', '-p', 'python3.11', '.'])

    subprocess.run(['source', 'bin/activate'], shell=True)

    # Install requirements
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    # Deactivate the virtual environment
    subprocess.run(['deactivate'], shell=True)

    os.chdir(source_folder)