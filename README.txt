==============
Pyramid_health
==============

Pyramid_health implement the pyramid view used by the loadbalancers to
perform health-check on the application.

Features ::

* Maintenance mode (enabled by touching a file)

Note::

* The health-check url is currently hard-coded to /health


Usage
=====

To use pyramid_health, you should include the module pyramid_health to
your pyramid configuration ::

   config.include("pyramid_health")

Or add  in the paster configuration

   pyramid.include = pyramid_health


Configuration options
=====================


healthcheck.disablefile ::

   Enable maintenance mode depending on the existance of a file.
   In maintenance mode, the health view responds with a 503 HTTP code.
