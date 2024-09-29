import json
import os
import re
from typing import Any, List, Tuple

from dotenv import load_dotenv, set_key
import nbformat as nbf

from .logger import LOGGER



PATH_DOTENV = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    ".env"
)

load_dotenv(PATH_DOTENV)



PATH_DOTENV_NAME = "PATH_DOTENV"
PATH_HISTORY_NAME = "PATH_HISTORY"
OPENAI_API_KEY_NAME = "OPENAI_API_KEY"
PATH_NOTEBOOK_NAME = "PATH_NOTEBOOK"

ENV_VARS = [
    PATH_DOTENV_NAME,
    PATH_HISTORY_NAME,
    OPENAI_API_KEY_NAME,
    PATH_NOTEBOOK_NAME
]

REGEX_SPLITTER = re.compile("```([^\n]*\n)(.*?)```", re.DOTALL | re.IGNORECASE)


class NotebookPathNotSpecified(ValueError):
    pass


def showenv():
    env_txt = json.dumps(
        {
            key: os.environ[key]
            for key in ENV_VARS
            if key in os.environ
        },
        indent=4
    )
    LOGGER.info(f"environment now set to:\n{env_txt}.")


def launch():
    os.system(f"jupyter notebook {os.environ[PATH_NOTEBOOK_NAME]}")


def update_env(key: str, val: Any) -> None:
    set_key(PATH_DOTENV, key, str(val))
    os.environ[key] = str(val)
    showenv()


def set_openai_api_key(val: str) -> None:
    update_env(OPENAI_API_KEY_NAME, val)


def get_user_home_folder() -> str:
    return os.path.expanduser("~")


def remove_code_markup(response: str) -> str:
    parts = []
    for language, code in REGEX_SPLITTER.findall(response):
        if language and language.strip() != "python":
            continue
        parts.append(code)
    return "".join(parts)


def new_notebook(path: str) -> None:
    if not path:
        raise NotebookPathNotSpecified()
    if not path.endswith(".ipynb"):
        LOGGER.warn("the path specified for the notebook does not contain "
                    "a recognizable extension. It is recommended to use the "
                    ".ipynb extension for notebooks.")
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        LOGGER.warn("all or some destination folders missing. Will "
                    "created them.")
        os.makedirs(folder, exist_ok=True)

    nb = nbf.v4.new_notebook()

    text = """# A plytonic-based notebook

This is an auto-generated template that imports the required
dependencies in order to interact programmatically with the notebook
using output from an LLM."""

    code = """%load_ext autoreload
%autoreload
from plytonic import CONV, PY, TXT, new_notebook, set_openai_api_key"""

    nb['cells'] = [nbf.v4.new_markdown_cell(text),
                   nbf.v4.new_code_cell(code)]

    with open(path, 'w') as f:
        nbf.write(nb, f)

    update_env(PATH_NOTEBOOK_NAME, path)


def validate_history_value(history: int) -> bool:
    if not isinstance(history, int) \
    or history < 0:
        raise ValueError("The argument for keyword parameter `history` must "
                         "be an integer equal to 0 or greater than that, got"
                         f"\"{history}\" instead.")
    return True





# fill environment variables with default values in case the .env
# file doesn't contain definitions for those variables yet:

if PATH_DOTENV_NAME not in os.environ:
    update_env(PATH_DOTENV_NAME, PATH_DOTENV)

if PATH_HISTORY_NAME not in os.environ:
    path_history = os.path.join(
        get_user_home_folder(),
        "plytonic",
        "history.json"
    )
    update_env(PATH_HISTORY_NAME, path_history)

if OPENAI_API_KEY_NAME not in os.environ:
    LOGGER.warn("could not find an OpenAI API key, please provide one by "
                "calling function `plytonic.util.set_openai_api_key(KEY)`.")





