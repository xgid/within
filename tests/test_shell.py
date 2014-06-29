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
            print("Error: could not delete {0}".format(filepath))

    while TEMP_DIRS:
        directory = None

        try:
            directory = TEMP_DIRS.pop()

            os.rmdir(directory)
        except OSError as exception:
            print("Error: could not delete {0}".format(directory))


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

    with working_directory(TEMP_DIRS[0]) as the_directory:
        assert the_directory == TEMP_DIRS[0]

        if 0 != os.system('touch {0}'.format(tempfile_a)):
            raise IOError("couldn't set up test")

        os.path.isdir(tempfile_a)

        with working_directory(TEMP_DIRS[1]):
            if 0 != os.system('touch {0}'.format(tempfile_a)):
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
        An exception that nothing else.
        """
        pass

    try:
        assert os.getcwd() == directory

        with working_directory(TEMP_DIRS[0]):
            if 0 != os.system('touch {0}'.format(tempfile_a)):
                raise IOError("couldn't set up test")

            os.path.isdir(tempfile_a)

            try:
                with working_directory(TEMP_DIRS[1]):
                    if 0 != os.system('touch {0}'.format(tempfile_a)):
                        raise IOError("couldn't set up test")

                    os.path.isdir(tempfile_b)

                    raise UniqueTestingException
            except UniqueTestingException:
                os.path.isdir(tempfile_a)

                raise

    except UniqueTestingException:
        assert os.getcwd() == directory


def test_temporary_directory_no_files():
    """
    Test that temporary_directory makes and deletes directories.
    """
    from within.shell import temporary_directory

    with temporary_directory() as tempdir:
        temp = tempdir

        assert os.path.isdir(temp)

    assert not os.path.isdir(temp)


def test_temporary_directory_with_files():
    """
    Test that temporary_directory deletes directories when they contain
    files.
    """
    from within.shell import temporary_directory

    with temporary_directory() as tempdir:
        temp = tempdir

        assert os.path.isdir(temp)

        for filename in ('foo', 'bar', 'baz'):
            filepath = os.path.join(temp, filename)

            with open(filepath, 'w') as fileobj:
                fileobj.write('this file contains something')

            assert os.path.isfile(filepath)

    assert not os.path.isdir(temp)


def test_temporary_directory_directories():
    """
    Test that nested directories are deleted
    """
    from within.shell import temporary_directory

    with temporary_directory() as tempdir:
        temp = tempdir

        assert os.path.isdir(temp)

        directory = os.path.join(temp, 'lorem')

        os.mkdir(directory)

        for filename in ('foo', 'bar', 'baz'):
            filepath = os.path.join(directory, filename)

            with open(filepath, 'w') as fileobj:
                fileobj.write('this file contains something')

            assert os.path.isfile(filepath)

    assert not os.path.isdir(temp)


def test_temporary_directory_exception():
    """
    Test that temporary_directory deletes files in exceptional cases,
    and doesn't eat exceptions
    """
    from within.shell import temporary_directory

    class TestException(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __eq__(self, other):
            return isinstance(other, TestException) and other.msg == self.msg

    try:
        with temporary_directory() as tempdir:
            temp = tempdir

            assert os.path.isdir(temp)

            for filename in ('foo', 'bar', 'baz'):
                filepath = os.path.join(temp, filename)

                with open(filepath, 'w') as fileobj:
                    fileobj.write('this file contains something')

                assert os.path.isfile(filepath)

                raise TestException("This is my error message")
    except TestException as exception:
        assert exception == TestException("This is my error message")
    else:
        raise AssertionError("exception was lost")

    assert not os.path.isdir(temp)
