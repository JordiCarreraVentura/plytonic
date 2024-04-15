import os

from nbformat import v4 as nbf, write as nbf_write

from __init__ import OperativeSystem, UnsupportedPlatformError, PLATFORM
from llms import CHATGPT
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
    cell = f"""{df_name} = pd.read_csv("{csv_path}")"""
    return nbf.new_code_cell(cell)


def add_query_func_def(cells: list[object]) -> None:
    func_def_cell = """def create_new_cell(cell_text: str):
    from IPython.core.getipython import get_ipython
    shell = get_ipython()
    payload = dict(
        source='set_next_input',
        text=cell_text,
        replace=False,
    )
    shell.payload_manager.write_payload(payload, single=False)

def query(cell_idx, prompt, df_out=''):
    context = _ih[cell_idx] if cell_idx else ''
    cell_text = query_engine(
        context=context,
        query=prompt,
        df_out=df_out
    )
    return cell_text

class Query:
    def __init__(self):
        return
    def __call__(self, cell_idx, prompt, df_out=''):
        create_new_cell(query(cell_idx, prompt, df_out=df_out))

Q = Query()"""
    cells.append(nbf.new_code_cell(func_def_cell))


def add_autoreload(cells):
    func_autoreload = """%load_ext autoreload
%autoreload"""
    cells.append(nbf.new_code_cell(func_autoreload))



def add_dependencies(cells):
    func_autoreload = """from nbformat import v4 as nbf
import pandas as pd

from notebook_utils import query_engine"""
    cells.append(nbf.new_code_cell(func_autoreload))



def make_notebook(**kwargs):

    params = dict(kwargs.items())

    csv_path = params['csv']
    df_name  = params['df_name'] if 'df_name' in params else 'df'
    nb_path  = params['nb_path'] if 'nb_path' in params else None
    
    cells = []

    add_autoreload(cells)
    add_dependencies(cells)
    add_query_func_def(cells)

    nb = nbf.new_notebook()

    if csv_path:
        cells.append(make_csv_input_cell(csv_path, df_name))

    if not cells:
        LOGGER.warn('Notebook contains no cells. There is nothing to do.')

    nb.cells.extend(cells)
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
        nbf_write(nb, f)
    
    return final_path



class QueryEngine:

    def __init__(self):
        return

    def __call__(
        self,
        context:   str,
        query:     str,
        df_out:    str = '',
        code_only: bool =True,
        run:       bool = False
    ) -> str:
        
        requirement = 'Given the code below, modify it so that it meets ' + \
                       f'the following requirements: "{query}".'

        _code_only = ' Please, return only the code, do not add any explanations ' \
                     'or verbal output.' if code_only else ''
        
        subject    = f'\n\nHere\'s the code:\n\n{context}'

        prompt = f'{requirement}{_code_only}\n\n{subject}'

        if run:
            pass
    
        answer = CHATGPT(prompt)
        return answer

query_engine = QueryEngine()