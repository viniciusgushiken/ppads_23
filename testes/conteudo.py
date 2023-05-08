import unittest
from flask import Flask, session
import app, aicontent

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.secret_key = 'secret_key'

        # Define aqui os valores da sessão, caso necessário
        # Exemplo:
        # with self.app.test_request_context():
        #     session['usr'] = 'example_user'
        #     session['refresh'] = 'example_token'

    def tearDown(self):
        pass

    def test_email_marketing_route_with_session(self):
        with self.app.test_client() as client:
            with self.app.test_request_context():
                # Define aqui os valores da sessão, caso necessário
                # Exemplo:
                # session['usr'] = 'example_user'
                # session['refresh'] = 'example_token'

                response = client.get('/email-marketing')
                self.assertEqual(response.status_code, 200)

    def test_email_marketing_route_without_session(self):
        with self.app.test_client() as client:
            response = client.get('/email-marketing')
            self.assertEqual(response.status_code, 302) # redirect code

    def test_run_ai_route(self):
        with self.app.test_client() as client:
            # Define aqui os valores de entrada para o método runAi, caso necessário
            # Exemplo:
            # input = 'exemplo de entrada'
            # category = 'categoria exemplo'
            # response = runAi(input, category)

            response = client.post('/run-ai', data=dict(
                input=input,
                category=category
            ))
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
