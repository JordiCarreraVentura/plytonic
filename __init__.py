import platform
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
