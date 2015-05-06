import os

from pyramid.response import Response
from pyramid.httpexceptions import HTTPServiceUnavailable


def includeme(config):
    config.add_route('healthcheck', '/health')
    config.add_view(health, route_name='healthcheck')


def health(request):
    settings = request.registry.settings

    if 'healthcheck.disablefile' in settings:
        if os.path.exists(settings['healthcheck.disablefile']):
            return HTTPServiceUnavailable(
                explanation='Healthcheck disabled by config')

    return Response('OK', content_type='text/plain')
