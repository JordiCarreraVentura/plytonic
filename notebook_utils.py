import os

import nbformat

from __init__ import OperativeSystem, UnsupportedPlatformError, PLATFORM
from logger import LOGGER


ENV     = os.environ
CSV     = ENV['csv']     if 'csv'      in ENV else None
DF_NAME = ENV['df_name'] if 'df_name'  in ENV else 'df_def'
NB_PATH = ENV['nb_path'] if 'nb_path'  in ENV else None



class MissingNotebookNameParameter(IOError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NotebookPathCollisionError(IOError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def make_default_name_by_platform():
    if PLATFORM is OperativeSystem.Linux \
    or PLATFORM is OperativeSystem.Mac:
        folder = '/tmp'
    else:
        raise UnsupportedPlatformError(PLATFORM.name)
    
    pid = os.getpid()
    while True:
        fullpath = os.path.join(folder, f'{pid}.ipynb')
        if not os.path.exists(fullpath):
            break

    return fullpath


def make_csv_input_cell():
    cell = f"""
import pandas as pd
{DF_NAME} = pd.read_csv({CSV})
    """
    return nbformat.v4.new_code_cell(source=cell)


def make_notebook():
    
    nb = nbformat.v4.new_notebook()
    
    if CSV:
        nb.cells.append(make_csv_input_cell())

    return write(nb)




def write(nb) -> str:
    if not nb.cells:
        LOGGER.warn('Notebook contains no cells. There is nothing to do.')

    if not NB_PATH:
        final_path = make_default_name_by_platform()
        LOGGER.warn(
            'No location was specified for the session notebook. '
            f'Using default value: {final_path}'
        )
    elif os.exists(NB_PATH):
        raise NotebookPathCollisionError(NB_PATH)
    else:
        full_path  =  os.path.realpath(NB_PATH)
        folder     =  os.dirname(full_path)
        filename   =  os.path.basename(full_path)
        os.makedirs(folder, exist_ok=True)
        final_path =  os.path.join(folder, filename)
        LOGGER(f'Saving notebook in "{final_path}"...')

    with open(final_path, "w") as f:
        nbformat.write(nb, f)
    
    return final_path
