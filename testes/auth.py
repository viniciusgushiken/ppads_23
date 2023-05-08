import unittest
from app import app

class SignupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_signup_success(self):
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'password123'
        }
        response = self.app.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please verify your email address', response.data)

    def test_signup_fail(self):
        data = {
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'password': 'pass'
        }
        response = self.app.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Falha ao se cadastrar', response.data)
