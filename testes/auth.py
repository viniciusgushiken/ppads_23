import unittest
from app import app

class SignupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_signup_success(self):
        data = {
            'name': 'teste',
            'email': 'teste@example.com',
            'password': 'password123'
        }
        response = self.app.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please verify your email address', response.data)

    def test_signup_fail(self):
        data = {
            'name': 'teste2',
            'email': 'teste2@example.com',
            'password': 'pass'
        }
        response = self.app.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Falha ao se cadastrar', response.data)


class LoginTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_login_success(self):
        # Testa se o login é bem sucedido com um usuário já cadastrado
        response = self.app.post('/login', data=dict(email='user1@test.com', password='senha1'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bem-vindo, user1@test.com', response.data)

    def test_login_unverified_email(self):
        # Testa se o login é bloqueado quando a conta do usuário não foi verificada
        response = self.app.post('/login', data=dict(email='user2@test.com', password='senha2'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Confirme seu cadastro no email antes de fazer login', response.data)

    def test_login_wrong_credentials(self):
        # Testa se o login é bloqueado quando as credenciais estão incorretas
        response = self.app.post('/login', data=dict(email='user1@test.com', password='senha_errada'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuario nao encontrado ou senha incorreta!', response.data)
        pass 
