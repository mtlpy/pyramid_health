import unittest
import tempfile

import webtest
from pyramid.config import Configurator


class TestSimple(unittest.TestCase):

    def setup(self, url=None, maintenance_code=None, failure_code=None,
              disablefile=None):

        config = Configurator()

        if url is not None:
            config.add_settings({'healthcheck.url': url})
        if maintenance_code is not None:
            config.add_settings(
                {'healthcheck.maintenance_code': maintenance_code})
        if disablefile is not None:
            config.add_settings({'healthcheck.disablefile': disablefile})

        config.include('pyramid_health')

        self.app = webtest.TestApp(config.make_wsgi_app())

    def test_get(self):
        self.setup()
        response = self.app.get('/health', status=200)
        self.assertEqual(response.body, 'OK')

    def test_post(self):
        self.setup()
        response = self.app.post('/health', status=200)
        self.assertEqual(response.body, 'OK')

    def test_url_get(self):
        self.setup(url='/whatsup')
        response = self.app.get('/whatsup', status=200)
        self.assertEqual(response.body, 'OK')

    def test_get_maintenance_on(self):
        tmpfile = tempfile.NamedTemporaryFile()
        self.setup(disablefile=tmpfile.name)

        response = self.app.get('/health', status=503)
        self.assertEqual(response.body, 'MAINTENANCE')

    def test_get_maintenance_on_code(self):
        tmpfile = tempfile.NamedTemporaryFile()
        self.setup(disablefile=tmpfile.name, maintenance_code=299)

        response = self.app.get('/health', status=299)
        self.assertEqual(response.body, 'MAINTENANCE')

    def test_get_maintenance_off(self):
        tmpfile = tempfile.NamedTemporaryFile()
        self.setup(disablefile=tmpfile.name)

        tmpfile.close()  # Remove the disablefile

        response = self.app.get('/health', status=200)
        self.assertEqual(response.body, 'OK')


class TestChecks(unittest.TestCase):

    def setup(self, failure_code=None):
        from pyramid_health import HealthCheckEvent

        self.check1_status = 'OK'
        self.check1_message = 'report1'

        def check1(event):
            event.report(name='check1',
                         status=self.check1_status,
                         message=self.check1_message)

        self.check2_status = 'OK'
        self.check2_message = 'report2'

        def check2(event):
            event.report(name='check2',
                         status=self.check2_status,
                         message=self.check2_message)
        config = Configurator()
        if failure_code is not None:
            config.add_settings({'healthcheck.failure_code': failure_code})
        config.include('pyramid_health')
        config.add_subscriber(check1, HealthCheckEvent)
        config.add_subscriber(check2, HealthCheckEvent)

        self.app = webtest.TestApp(config.make_wsgi_app())

    def test_param(self):
        self.setup()
        self.check1_status = 'NOK'

        response = self.app.get('/health?checks=all', status=503)
        self.assertEqual(response.body, 'ERROR')

        response = self.app.get('/health?checks=true', status=503)
        self.assertEqual(response.body, 'ERROR')

        response = self.app.get('/health', status=200)
        self.assertEqual(response.body, 'OK')

    def test_ok(self):
        self.setup()
        response = self.app.get('/health?checks=all', status=200)
        self.assertEqual(response.body, 'OK')

    def test_check1_nok(self):
        self.setup()
        self.check1_status = 'NOK'
        self.check1_message = 'kaputt!'

        response = self.app.get('/health?checks=all', status=503)
        self.assertEqual(response.body, 'ERROR')

    def test_check2_nok(self):
        self.setup()
        self.check2_status = 'NOK'
        self.check2_message = 'nope'

        response = self.app.get('/health?checks=all', status=503)
        self.assertEqual(response.body, 'ERROR')

    def test_no_message(self):
        self.setup()
        self.check2_status = 'NOK'
        self.check2_message = None

        response = self.app.get('/health?checks=all', status=503)
        self.assertEqual(response.body, 'ERROR')

    def test_all_nok(self):
        self.setup()
        self.check1_status = 'NOK'
        self.check2_status = 'NOK'

        response = self.app.get('/health?checks=all', status=503)
        self.assertEqual(response.body, 'ERROR')

    def test_nok_failure_code(self):
        self.setup(failure_code=500)

        self.check1_status = 'NOK'

        response = self.app.get('/health?checks=all', status=500)
        self.assertEqual(response.body, 'ERROR')
