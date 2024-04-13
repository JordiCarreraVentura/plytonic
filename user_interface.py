from argparse import ArgumentParser
import os


UI_HELP_READ = 'Path to a CSV file to read input data from.'


class ParameterVariableNameCollision(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserInterfaceLauncher:

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('--csv', type=str, help=UI_HELP_READ)
        #self.parser.add_argument('--PWD', type=str, help=UI_HELP_READ)
    
    def __call__(self):
        args = self.parser.parse_args()
        for argname, argval in args.__dict__.items():
            if argname in os.environ:
                raise ParameterVariableNameCollision(argname)
            if not argval:
                continue
            os.environ[argname] = argval
