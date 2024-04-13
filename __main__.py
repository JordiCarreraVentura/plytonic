from user_interface import UserInterfaceLauncher
import os


if __name__ == '__main__':

    ui = UserInterfaceLauncher()
    print(os.environ)
    ui()
    print(os.environ)