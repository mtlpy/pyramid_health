==============
Pyramid_health
==============

Simple healthcheck endpoint for Pyramid, with maintenance mode.


Installation
============

Install using setuptools, e.g. (within a virtualenv)::

  $ pip install pyramid_health


Setup
=====

Once ``pyramid_health`` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration.  In your
Pyramid project's ``__init__.py``:

.. code-block:: python

   config = Configurator(.....)
   config.include('pyramid_health')

Alternately you can use the ``pyramid.includes`` configuration value in your
``.ini`` file:

.. code-block:: ini

   [app:myapp]
   pyramid.includes = pyramid_health


Usage
=====

Pyramid_health configuration (values are defaults):

.. code-block:: ini

   [app:myapp]
   healthcheck.disablefile = /tmp/maintenance  # touch this file to activate


Maintenance mode
================

In maintenance mode, the healthcheck endpoint's response is changed to inform
the HTTP client that this backend is unavailable. Typically a loadbalancer
polling the backends would stop sending traffic to a backend in maintenance
mode.

Currently, the healthcheck endpoint responds ``503 Service Unavailable`` in
maintenance mode.


TODO
====

- Add a setting healthcheck.url (currently hardcoded as ``/health``)
- Add a setting to change maintenance mode response
