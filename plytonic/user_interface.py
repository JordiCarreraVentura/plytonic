from argparse import ArgumentParser
import os

from notebook_utils import make_notebook


UI_HELP_CSV    = 'Path to a CSV file to read input data from.'

UI_HELP_DFNAME = 'Name of the `DataFrame` variable assigned to the data read ' \
               + 'during initialization.'

UI_HELP_NBPATH = "Path where the custom notebook created for the new session ' \
               + 'will be written to."

UI_HELP_KERNEL = "Name of the kernel for installing plytonic's dependencies " \
                 "and where the notebook will be run from."


class ParameterVariableNameCollision(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserInterfaceLauncher:

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('--csv',         type=str, help=UI_HELP_CSV   )
        self.parser.add_argument('--nb_path',     type=str, help=UI_HELP_NBPATH)
        self.parser.add_argument('--df_name',     type=str, help=UI_HELP_DFNAME)
        self.parser.add_argument('--kernel_name', type=str, help=UI_HELP_KERNEL, default='plytonic_env')
        
        filepath    =  os.path.realpath(__file__)
        folder      =  os.path.dirname(filepath)
        os.environ['WORKDIR'] = folder


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
        notebook    =  make_notebook(**os.environ)
        kernel_name =  os.environ['kernel_name']

        origin = os.getcwd()
        os.chdir(os.environ['WORKDIR'])
        # print(os.environ['WORKDIR'])
        # exit()

        activate    = f"source {os.path.dirname(os.environ['WORKDIR'])}/bin/activate"
        install     = f'pip install -r {os.path.dirname(os.environ["WORKDIR"])}/requirements.txt'
        deactivate  = "deactivate"
        kernelize   = "plytonic_env_installed=`jupyter kernelspec list " \
"""| grep plytonic_env | wc -l | awk '{print $1}'`; if [ $plytonic_env_installed -eq 0 ] ; 
    then python -m ipykernel install --user --name """ \
"'" + kernel_name + "' --display-name '" + kernel_name + "'; fi"

        os.system(f'{activate}; {install}; {kernelize}; {deactivate}')
        os.chdir(origin)
        os.system(f'jupyter notebook "{notebook}" ' 
                  f'--MultiKernelManager.default_kernel_name="{kernel_name}"')
