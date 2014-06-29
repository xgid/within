"""
Shell context managers.
"""
from contextlib import contextmanager
import os
from tempfile import mkdtemp


@contextmanager
def working_directory(directory):
    """
    Do operations within a given working directory.

    directory: The directory to set as the current working directory.
    """
    old_directory = os.getcwd()

    try:
        os.chdir(directory)

        yield directory
    finally:
        os.chdir(old_directory)


@contextmanager
def temporary_directory():
    """
    Create a temporary directory that will be emptied and deleted on
    context manager exit. Returns the string path to the directory.
    """
    tempdir = mkdtemp()

    try:
        yield tempdir
    finally:
        remove_directory(tempdir)


def remove_directory(directory):
    """
    Recursively delete a directory.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)

        if os.path.isdir(path):
            remove_directory(path)
        else:
            os.remove(path)

    os.rmdir(directory)
