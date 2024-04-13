from argparse import ArgumentParser
import os

from notebook_utils import make_notebook


UI_HELP_CSV    = 'Path to a CSV file to read input data from.'

UI_HELP_DFNAME = 'Name of the `DataFrame` variable assigned to the data read ' \
               + 'during initialization.'

UI_HELP_NBPATH = "Path where the custom notebook created for the new session ' \
               + 'will be written to."



class ParameterVariableNameCollision(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserInterfaceLauncher:

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('--csv',     type=str, help=UI_HELP_CSV   )
        self.parser.add_argument('--nb_path', type=str, help=UI_HELP_NBPATH)
        self.parser.add_argument('--df_name', type=str, help=UI_HELP_DFNAME)
    
    def __call__(self):
        args = self.parser.parse_args()
        for argname, argval in args.__dict__.items():
            if argname in os.environ:
                raise ParameterVariableNameCollision(argname)
            if not argval:
                continue
            os.environ[argname] = argval
        self.__launch()
    
    def __launch(self):
        notebook = make_notebook()
        os.system(f'jupyter notebook {notebook}')
