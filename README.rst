==============
Pyramid_health
==============

Simple healthcheck endpoint for Pyramid, with maintenance mode and application
checks.

* PyPI: https://pypi.python.org/pypi/pyramid_health
* Bitbucket: https://bitbucket.org/Ludia/pyramid_health
* |droneio|

.. |droneio| image::
   https://drone.io/bitbucket.org/Ludia/pyramid_health/status.png
   :target: https://drone.io/bitbucket.org/Ludia/pyramid_health
   :alt: Tests on drone.io


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
   healthcheck.url = /health

   healthcheck.disablefile = /tmp/maintenance  # touch this file to activate

   healthcheck.maintenance_code = 503  # Code to return in maintenance mode

   healthcheck.failure_code = 503  # Code to return when one or more checks fail


Operation
=========

When your application is healthy, pyramid_health endpoint returns ``200 OK``.
When you enable the maintenance mode, the endpoint returns ``503 MAINTENANCE``
and logs ``Health response: MAINTENANCE``.
If at least one application check return an error, the endpoint returns
``503 ERROR`` and logs ``Health response: ERROR (<all-check-results>)``.


Application checks
==================

To add an application check:

.. code-block:: python

   from pyramid.events import subscriber
   from pyramid_health import HealthCheckEvent


   @subscriber(HealthCheckEvent)
   def db_check(event):
       try:
           db.ping()
       except:
           event.report_check_result(name='db',
                                     status='NOK',
                                     message='ping failed')
       else:
           event.report_check_result(name='db', status='OK')


Notes:

- You may or may not report succeeding checks


Maintenance mode
================

In maintenance mode, the healthcheck endpoint's response is changed to inform
the HTTP client that this backend is unavailable. Typically a loadbalancer
polling the backends would stop sending traffic to a backend in maintenance
mode.

The response status code is ``503 MAINTENANCE`` by default. You can
change it with ``healthcheck.maintenance_code``.
