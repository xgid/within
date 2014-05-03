"""
Database context managers.
"""
from contextlib import contextmanager


@contextmanager
def manage(connection, commit_on_close=False):
    """
    Manage a connection to a database ensuring that a commit occurs as
    necessary, and ensures the connection gets closed.

    connection: A dbapi compatible connection object.
    commit_on_close: (optional, False) Commit changes when closing the
        database.
    """
    try:
        cursor = connection.cursor()

        yield cursor

        if commit_on_close:
            connection.commit()
    finally:
        cursor.close()
        connection.close()
