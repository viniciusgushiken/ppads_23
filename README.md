# ppads_23 - Manual do Usuário
Projeto final da matéria Prática Profissional em Análise e Desenvolvimento de Sistemas.

A stack utilizada nesse projeto é Python, Flask, Firebase e OpenAI.


Para o funcionamento da aplicação localmente. Após clonar o repositório localmente,

1. É necessário instalar as dependências necessárias com o comando

`pip install -r requirements.txt`

2. Crie um arquivo `config.py` com as suas credenciais do Firebase e a sua chave da OpenAi. Vale ressaltar que tanto o Firebase quanto a OpenAi é
 possível criar as chaves de forma gratuita.
 
 ```
 class Config(object):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY = "this-is-a-super-secret-key"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}

## Enter your Open API Key here
OPENAI_API_KEY = <sua-chave-api>

## Firebase
firebaseConfig = {
  'apiKey': "<sua-chave-api>",
  'authDomain': "<sua-domain-domain>",
  'databaseURL': "<sua-database-url>",
  'projectId': "<seu-project-id>",
  'storageBucket': "<sua-storageBucket>",
  'messagingSenderId': "<sua-messagingSenderId>",
  'appId': "<sua-appId>",
  'measurementId': "<sua-measurementId>"
}
 ```
 
3. Após isso, basta rodar no seu terminal o comando. Isso deverá abrir o aplicação localmente.

`python3 flask run`
