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

    if 'health.maintenance.file' in settings:
        if os.path.exists(settings['health.maintenance.file']):
            return HTTPServiceUnavailable()

    return Response('OK', content_type='text/plain')
