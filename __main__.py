from user_interface import UserInterfaceLauncher
import os

# from __init__ import PATH_INPUT
# from client import ChatGptClient, ZephyrClient
# from utils import read_txt


if __name__ == '__main__':

    ui = UserInterfaceLauncher()
    print(os.environ)
    ui()
    print(os.environ)

    #os.system('jupyter notebook')