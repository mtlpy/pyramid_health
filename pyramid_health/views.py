from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name='healthcheck')
def health(request):
    """Always returns HTTP 200 OK.

    For human-friendliness, a body containing 'OK' is also returned.
    """
    return Response('OK', content_type='text/plain')
