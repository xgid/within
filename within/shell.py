"""
Shell context managers.
"""
from contextlib import contextmanager
import os


@contextmanager
def working_directory(directory):
    """
    Do operations within a given working directory.

    directory: The directory to set as the current working directory.
    """
    old_directory = os.getcwd()

    try:
        os.chdir(directory)

        yield
    finally:
        os.chdir(old_directory)
