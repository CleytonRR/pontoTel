import unittest
import time
import json
from app import app

mockValidSymbol = 'PETR4.SA'
mockValidName = 'Petrobras'
mockInvalidName = 'invalid_company'
mockInvalidSymbol = 'invalid_symbol'
id_company = ''
id = ''

mockUser = "any_user"
mockUserInvalid = "invalid_user"
mockUserNewName = 'new_name'

class UserCreate(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.post('/v1/user/',
                                      data=json.dumps(dict(nome=mockUser)),
                                      content_type='application/json')

    def test_post(self):
        self.assertEqual(201, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class UserGetByName(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.get('v1/user/{}/'.format(mockUser))

    def test_data(self):
        self.assertIn(mockUser, str(self.response.data))

    def test_code(self):
        self.assertEqual(200, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class UserGetByNameError(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.get('v1/user/{}/'.format(mockUserInvalid))

    def test_code(self):
        self.assertEqual(400, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class UserPut(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.put('v1/user/{}/'.format(mockUser),
                                     data=json.dumps(dict(nome=mockUserNewName)),
                                      content_type='application/json')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class UserPutError(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.put('v1/user/{}/'.format(mockUserInvalid),
                                     data=json.dumps(dict(nome=mockUserNewName)),
                                      content_type='application/json')

    def test_get(self):
        self.assertEqual(400, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class AddCompanyForUser(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.post('v1/company/',
                                 data=json.dumps(dict(name=mockValidName, symbol=mockValidSymbol, user=mockUserNewName)),
                                 content_type='application/json')
        datas = json.loads(self.response.data)
        global id_company
        id_company = datas['id']
    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class AddCompanyForUserError(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.post('v1/company/',
                                 data=json.dumps(dict(name=mockValidName, symbol=mockValidSymbol, user=mockInvalidName)),
                                 content_type='application/json')
    def test_get(self):
        self.assertEqual(400, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class GetCompanyById(unittest.TestCase):
    def setUp(self):
        self.app_test = app.test_client()
        self.response = self.app_test.get('/v1/company/{}/'.format(id_company))
        self.datas = json.loads(self.response.data)

    def test_data(self):
        self.assertEqual(mockValidName, self.datas['company'])

    def test_delete(self):
        self.response_delete = self.app_test.delete('/v1/company/{}/'.format(id_company))
        self.assertEqual(204, self.response_delete.status_code)

    def tearDown(self):
        time.sleep(15)

class GetCompanyByIdError(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.get('/v1/company/{}/'.format(id_company + 1))
        self.datas = json.loads(self.response.data)

    def test_get(self):
        self.assertEqual(400, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

class UserDeleteError(unittest.TestCase):
    def setUp(self):
        app_test = app.test_client()
        self.response = app_test.delete('v1/user/{}/'.format(mockUserInvalid))

    def test_delete(self):
        self.assertEqual(400, self.response.status_code)

    def tearDown(self):
        time.sleep(15)

if __name__ == '__main__':
    unittest.main()