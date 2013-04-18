def includeme(config):
    """Configure a route and view for AWS ELB health check.

    The route name and URI pattern are not configurable for now,
    please open a feature request if you need that.
    """
    config.add_route('healthcheck', '/health')
    config.scan('pyramid_health.views')
