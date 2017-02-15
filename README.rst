django-laterpay
======================

.. image:: https://badge.fury.io/py/django-laterpay.png
    :target: http://badge.fury.io/py/django-laterpay

.. image:: https://travis-ci.org/laterpay/django-laterpay.png?branch=master
    :target: https://travis-ci.org/laterpay/django-laterpay

.. image:: https://coveralls.io/repos/laterpay/django-laterpay/badge.png?branch=master
    :target: https://coveralls.io/r/laterpay/django-laterpay


`LaterPay <http://www.laterpay.net/>`__ Django utilities

Installation
------------

::

    $ pip install django-laterpay

Usage
-----

See https://www.laterpay.net/developers/docs

Development
-----------

See https://github.com/laterpay/django-laterpay

`Tested by Travis <https://travis-ci.org/laterpay/django-laterpay>`__

Releasing checklist
-------------------

This repository uses `GitHub flow <https://guides.github.com/introduction/flow/index.html>`__.
In order to release a new version please follow these steps:

* Install ``twine`` with ``$ pipsi install twine``
* Ensure ``CHANGELOG`` is representative
* Determine next version number from the ``CHANGELOG`` (ensuring we follow `SemVer <http://semver.org/>`__)
* Update the ``CHANGELOG`` with the new version
* Update the version in ``setup.py``
* Update `trove classifiers <https://pypi.python.org/pypi?%3Aaction=list_classifiers>`_ in ``setup.py``
* Stage the change ``git add CHANGELOG.md setup.py``
* Commit and ensure the correct version number is part of the commit message ``git commit -m "Bump to 2.0.0"``
* Tag the commit with current version number ``git tag -s 2.0.0 -m "Bump to 2.0.0"``
* ``git push --tags origin master``
* ``python setup.py sdist bdist_wheel``
* ``twine upload dist/$newver`` or optionally, for signed releases ``twine upload -s ...``
* Bump version in ``setup.py`` to next likely version as ``Alpha 1`` (e.g. ``3.0.0a1``)
* Alter trove classifiers in ``setup.py``
* Add likely new version to ``CHANGELOG.md``
* Stage the change ``git add CHANGELOG.md setup.py``
* Commit ``git commit -m "Post release prep"``
