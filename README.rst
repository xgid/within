======
within
======
.. image:: https://travis-ci.org/bcj/within.svg?branch=master
.. image:: https://coveralls.io/repos/bcj/within/badge.png?branch=master
  :target: https://coveralls.io/r/bcj/within?branch=master

``within`` is a collection of context managers designed to make everyday tasks
simpler and safer to perform.

Instalation
===========
``within`` is in PyPI, so it can be installed directly using::

    $ pip install within

Usage
=====
Shell
-----
The ``working_directory`` context manager allows temporary changes to the
current working directory. Within the with statement, the path will be set to
the supplied working directory. As soon as the context is left (even in case
or errors) the working directory is restored. These context managers can be
nested as necessary::

    from within.shell import working_directory

    ...

    with working_directory("my/file/path"):
        assert os.getcwd() == "my/file/path"

The ``temporary_directory`` context manager allows for the creation of
temporary directories that only exist for the lifetime of the context manager.
On close (normal, or with an Exception), the directory will be emptied then
deleted. Exceptions will not be captured. The string path to the directory
is returned on instantiation::

    from within.shell import temporary_directory

    ...

    with temporary_directory() as tempdir:
        assert os.path.isdir(tempdir)

        directory = tempdir

    assert not os.path.isdir(directory)


For extra style points, why not combine the two context managers::

    from within.shell import temporary_directory, working_directory

    ...

    #Python 3 only. If on 2 use contextlib.nested
    with temporary_directory() as tempdir, working_directory(tempdir): 
        # do stuff

Database
--------
The `manage` context manager manages database connections, ensuring that
connections get closed::

    from within.db import manage

    ...

    with manage(sqlite3.connect(database)) as cursor:
        cursor.execute('SELECT * from table_name;')

Manage also provides an automatic way to commit changes on close::

    from within.db import manage

    ...

    with manage(sqlite3.connect(database), commit_on_close=True) as cursor:
        cursor.execute('INSERT into table_name (column) value ?;', (value,))

Development
===========
Active development occurs on `Github <https://github.com/bcj/within/>`_. Pull
and feature requests are welcome

Testing
-------
Testing is done under ``nose`` for python 2.7 and 3.4 and done by running the
``nose2.sh`` and ``nose3.sh`` scripts. Accepted code should have 100% coverage,
and, unless absolutely necessary, should pass pep8 standards and score 10.0 on
pylint (where possible, even tests should attain this).

License
=======
``within`` is released under an MIT license.
