from .settings import Settings
from os import system


def py_venv_command(command: str) -> None:
    system(f"{Settings.python_venv_path} {command}")
