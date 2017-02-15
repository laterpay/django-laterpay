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

* Ensure ``CHANGELOG`` is representative
* Determine next version number from the ``CHANGELOG`` (ensuring we follow `SemVer <http://semver.org/>`__)
* Update the ``CHANGELOG`` with the new version
* Update the version in ``setup.py``
* Tag the commit with current version number
* ``git push --tags origin master``
* ``python setup.py register sdist upload``
