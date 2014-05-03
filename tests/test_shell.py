"""
Tests for the shell context managers.
"""
from __future__ import print_function

import os
from tempfile import mkdtemp

from nose import with_setup


TEMP_DIRS = []
TEMP_FILES = []


def cleanup():
    """
    Make sure no temp files/folders exist.
    """
    while TEMP_FILES:
        filepath = None

        try:
            filepath = TEMP_DIRS.pop()

            os.remove(filepath)
        except OSError as exception:
            print("Error: could not delete {}".format(filepath))

    while TEMP_DIRS:
        directory = None

        try:
            directory = TEMP_DIRS.pop()

            os.rmdir(directory)
        except OSError as exception:
            print("Error: could not delete {}".format(directory))


@with_setup(cleanup, cleanup)
def test_working_directory():
    """
    Tests the working_directory context manager works as expected.
    """
    from within.shell import working_directory

    directory = os.getcwd()

    TEMP_DIRS.append(mkdtemp())
    TEMP_DIRS.append(mkdtemp())

    tempfile_a = os.path.join(TEMP_DIRS[0], 'filepath_a')
    tempfile_b = os.path.join(TEMP_DIRS[1], 'filepath_b')

    assert os.getcwd() == directory

    with working_directory(TEMP_DIRS[0]):
        if 0 != os.system('touch {}'.format(tempfile_a)):
            raise IOError("couldn't set up test")

        os.path.isdir(tempfile_a)

        with working_directory(TEMP_DIRS[1]):
            if 0 != os.system('touch {}'.format(tempfile_a)):
                raise IOError("couldn't set up test")

            os.path.isdir(tempfile_b)

        os.path.isdir(tempfile_a)

    assert os.getcwd() == directory


@with_setup(cleanup, cleanup)
def test_working_directory_failure():
    """
    Tests the working_directory context manager works with errors.
    """
    from within.shell import working_directory

    directory = os.getcwd()

    TEMP_DIRS.append(mkdtemp())
    TEMP_DIRS.append(mkdtemp())

    tempfile_a = os.path.join(TEMP_DIRS[0], 'filepath_a')
    tempfile_b = os.path.join(TEMP_DIRS[1], 'filepath_b')

    class UniqueTestingException(Exception):
        """
        An exception that nothing else
        """
        pass

    try:
        assert os.getcwd() == directory

        with working_directory(TEMP_DIRS[0]):
            if 0 != os.system('touch {}'.format(tempfile_a)):
                raise IOError("couldn't set up test")

            os.path.isdir(tempfile_a)

            try:
                with working_directory(TEMP_DIRS[1]):
                    if 0 != os.system('touch {}'.format(tempfile_a)):
                        raise IOError("couldn't set up test")

                    os.path.isdir(tempfile_b)

                    raise UniqueTestingException
            except UniqueTestingException:
                os.path.isdir(tempfile_a)

                raise

    except UniqueTestingException:
        assert os.getcwd() == directory
        pass  # everything went as expected
