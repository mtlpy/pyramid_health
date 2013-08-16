import unittest
import mock

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


class TestHealthMaintenance(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        settings = {'health.maintenance.file': '/maintenance/file/test'}
        config = Configurator(settings=settings)
        config.include('pyramid_health')
        self.app = webtest.TestApp(config.make_wsgi_app())

    @mock.patch("os.path.exists")
    def test_get_maintenance_on(self, m_exists):
        m_exists.return_value = True

        response = self.app.get('/health', expect_errors=True)

        m_exists.assert_called_with('/maintenance/file/test')

        self.assertEqual(response.status_int, 503)

    @mock.patch("os.path.exists")
    def test_get_maintenance_off(self, m_exists):
        m_exists.return_value = False

        response = self.app.get('/health')

        m_exists.assert_called_with('/maintenance/file/test')

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, b'OK')
