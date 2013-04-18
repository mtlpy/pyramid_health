import unittest

import webtest
from pyramid.config import Configurator


class TestHealth(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        settings = {}
        config = Configurator(settings=settings)
        config.include('pyramid_health')
        self.app = webtest.TestApp(config.make_wsgi_app())

    def test_get(self):
        response = self.app.get('/health')

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, b'OK')

    def test_post(self):
        response = self.app.post('/health')

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, b'OK')
