"""
Tests for the db context managers.
"""
from __future__ import print_function

import os
import sqlite3
from tempfile import mkdtemp

from nose import with_setup


SQLITE3_DIR = None
SQLITE3_FILENAME = 'sqlite3.db'


def setup_sqlite3():
    """
    Create a temp sqlite3 database.
    """
    global SQLITE3_DIR

    SQLITE3_DIR = mkdtemp()

    filepath = os.path.join(SQLITE3_DIR, SQLITE3_FILENAME)

    try:
        cursor = sqlite3.connect(filepath).cursor()

        cursor.execute("CREATE TABLE temp (key TEXT PRIMARY KEY, value TEXT);")
        cursor.execute("INSERT INTO temp (key, value) VALUES (?, ?);",
                       ('foo', 'bar'))

        cursor.connection.commit()

        cursor.close()
        cursor.connection.close()
    except:
        teardown_sqlite3()

        raise


def teardown_sqlite3():
    """
    Destroy a temp sqlite3 database.
    """
    global SQLITE3_DIR

    filepath = os.path.join(SQLITE3_DIR, SQLITE3_FILENAME)

    os.remove(filepath)

    os.rmdir(SQLITE3_DIR)

    SQLITE3_DIR = None


@with_setup(setup_sqlite3, teardown_sqlite3)
def test_manage():
    """
    Test that the connnection manager works properly.
    """
    from within.db import manage

    connection = sqlite3.connect(os.path.join(SQLITE3_DIR, SQLITE3_FILENAME))

    with manage(connection) as cursor:
        the_cursor = cursor  # save cursor for outside testing.

        cursor.execute('SELECT key, value FROM temp;')
        assert cursor.fetchall() == [('foo', 'bar')]

        # Make sure that writing doesn't happen
        cursor.execute('INSERT INTO temp (key, value) VALUES (?, ?);',
                       ('lorem', 'ipsum'))

    try:
        # shouldn't be possible if closed
        the_cursor.execute('SELECT key, value FROM temp;')
    except sqlite3.ProgrammingError:
        pass  # everything went as expected
    else:
        raise AssertionError("cursor not closed")

    try:
        connection.cursor()  # shouldn't be possible if closed
    except sqlite3.ProgrammingError:
        pass  # everything went as expected
    else:
        raise AssertionError("database not closed")

    # make sure nothing was added
    connection = sqlite3.connect(os.path.join(SQLITE3_DIR, SQLITE3_FILENAME))

    cursor = connection.cursor()

    cursor.execute('SELECT key, value FROM temp;')
    assert cursor.fetchall() == [('foo', 'bar')]

    cursor.close()
    connection.close()


@with_setup(setup_sqlite3, teardown_sqlite3)
def test_manage_commit():
    """
    Test that the connnection manager works properly with committing.
    """
    from within.db import manage

    connection = sqlite3.connect(os.path.join(SQLITE3_DIR, SQLITE3_FILENAME))

    with manage(connection, commit_on_close=True) as cursor:
        the_cursor = cursor  # save cursor for outside testing.

        cursor.execute('SELECT key, value FROM temp;')
        assert cursor.fetchall() == [('foo', 'bar')]

        cursor.execute('INSERT INTO temp (key, value) VALUES (?, ?);',
                       ('lorem', 'ipsum'))

    try:
        # shouldn't be possible if closed
        the_cursor.execute('SELECT key, value FROM temp;')
    except sqlite3.ProgrammingError:
        pass  # everything went as expected
    else:
        raise AssertionError("cursor not closed")

    try:
        connection.cursor()  # shouldn't be possible if closed
    except sqlite3.ProgrammingError:
        pass  # everything went as expected
    else:
        raise AssertionError("database not closed")

    # make sure something was added
    connection = sqlite3.connect(os.path.join(SQLITE3_DIR, SQLITE3_FILENAME))

    cursor = connection.cursor()

    cursor.execute('SELECT key, value FROM temp;')
    assert set(cursor.fetchall()) == set((('foo', 'bar'), ('lorem', 'ipsum')))

    cursor.close()
    connection.close()
