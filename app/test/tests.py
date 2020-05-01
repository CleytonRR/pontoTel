import unittest
import time
from app import app

mockValidSymbol = 'PETR4.SA'
mockInvalidSymbol = 'invalid_symbol'

class TestRouteBovespa(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.get('/v1/bovespa/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content_type(self):
        self.assertIn('application/json', self.response.content_type)

    def tearDown(self):
        time.sleep(15)

class TestRouteSearchByName(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        url = '/v1/busca/{}/'.format(mockValidSymbol)
        self.response = app_test.get(url)

    def test_content_type(self):
        self.assertIn('application/json', self.response.content_type)

    def tearDown(self):
        time.sleep(15)

class TestRouteSearchByNameError(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        url = '/v1/busca/{}/'.format(mockInvalidSymbol)
        self.response = app_test.get(url)

    def test_get(self):
        self.assertEqual(400, self.response.status_code)

    def test_content_type(self):
        self.assertIn('application/json', self.response.content_type)

    def tearDown(self):
        time.sleep(15)

if __name__ == '__main__':
    unittest.main()