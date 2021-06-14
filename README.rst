================
 FAI Python Lib
================

-------------------------------------
Library for FAI customization scripts
-------------------------------------

This Python lib eases the implementation of FAI_ customization scripts with a
high level of abstraction and resonable error handling. It is meant to be
``import``'ed in scripts run by ``fai-do-scripts(1)`` during an FAI
installation or softupdate.

.. _FAI: https://fai-project.org/


Documentation
=============

The documentation is based on Sphinx and can be built using make_:
``make doc``. Documentation sources are in the ``docs/`` directory.

Tests
=====

Tests reside in the ``tests/`` directory and are based on pytest_ and can be run
easily using make_: ``make test``

.. _pytest: https://docs.pytest.org/


.. _make:

Makefile
========

A ``Makefile`` is provided to ease testing and building Python packages. Run
``make help`` for usage hints.


Packaging and Releasing
=======================

This lib uses PEP 517/PEP 518-compatible packaging based on setuptools. All
project settings should normally go into ``setup.cfg``, while ``setup.py`` is mainly
provided for compatibility. The build system configuration resides in
``pyproject.toml``.

Each released version is tagged with a tag of the form ``release/x.y.z`` with
``x``, ``y``, and ``z`` being major, minor, and patch version, respectively, as
defined by `Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/
