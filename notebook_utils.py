import os

from nbformat import current as nbf

from __init__ import OperativeSystem, UnsupportedPlatformError, PLATFORM
from logger import LOGGER



class MissingNotebookNameParameter(IOError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NotebookPathCollisionError(IOError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def make_default_name_by_platform():
    if PLATFORM is OperativeSystem.Linux \
    or PLATFORM is OperativeSystem.Mac:
        folder = '.'
    else:
        raise UnsupportedPlatformError(PLATFORM.name)
    
    pid = os.getpid()
    while True:
        fullpath = os.path.join(folder, f'{pid}.ipynb')
        if not os.path.exists(fullpath):
            break

    return fullpath


def make_csv_input_cell(csv_path, df_name):
    cell = f"""
import pandas as pd

{df_name} = pd.read_csv("{csv_path}")
    """
    return nbf.new_code_cell(cell)


def make_notebook(**kwargs):

    params = dict(kwargs.items())

    csv_path = params['csv']
    df_name  = params['df_name'] if 'df_name' in params else 'df'
    nb_path  = params['nb_path'] if 'nb_path' in params else None

    nb = nbf.new_notebook()
    cells = []

    if csv_path:
        cells.append(make_csv_input_cell(csv_path, df_name))

    if not cells:
        LOGGER.warn('Notebook contains no cells. There is nothing to do.')

    nb['worksheets'].append(nbf.new_worksheet(cells=cells))
    final_path = write(nb, nb_path=nb_path)

    return final_path



def write(nb, nb_path='') -> str:

    if not nb_path:
        final_path = make_default_name_by_platform()
        LOGGER.warn(
            'No location was specified for the session notebook. '
            f'Using default value: {final_path}'
        )
    elif os.path.exists(nb_path):
        raise NotebookPathCollisionError(nb_path)
    else:
        full_path  =  os.path.realpath(nb_path)
        folder     =  os.dirname(full_path)
        filename   =  os.path.basename(full_path)
        os.makedirs(folder, exist_ok=True)
        final_path =  os.path.join(folder, filename)
        LOGGER(f'Saving notebook in "{final_path}"...')

    with open(final_path, "w") as f:
        nbf.write(nb, f, 'ipynb')
    
    return final_path
