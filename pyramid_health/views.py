import os

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPServiceUnavailable


@view_config(route_name='healthcheck')
def health(request):
    """Always returns HTTP 200 OK.

    For human-friendliness, a body containing 'OK' is also returned.
    """
    settings = request.registry.settings

    if 'healthcheck.disablefile' in settings:
        if os.path.exists(settings['healthcheck.disablefile']):
            return HTTPServiceUnavailable(
                explanation='Healthcheck disabled by config')

    return Response('OK', content_type='text/plain')
