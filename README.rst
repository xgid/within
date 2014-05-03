======
within
======
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
