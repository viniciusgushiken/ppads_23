import openai
import config
import app

openai.api_key = config.OPENAI_API_KEY

def runAi(input, category):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=input,
      temperature=0.8,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)

    if 'choices' in response:
        if len(response['choices']) > 0:
            answer = response['choices'][0]['text']

        else:
            answer = 'Opps sorry, you beat the AI this time'
    else:
        answer = 'Opps sorry, you beat the AI this time'

    # get current user id making the request
    user =  app.auth.get_account_info(app.session['usr'])
    id_token = user['users'][0]['localId']

    # data to be stored in the db
    data = {
        'user_id_token':id_token,
        'category':category,
        'prompt':input,
        'unix_created_at':response["created"],
        'open_ai_id':response["id"],
        'model':response["model"],
        'object':response["object"],
        'completion_tokens':response["usage"]["completion_tokens"],
        'prompt_tokens':response["usage"]["prompt_tokens"],
        'total_tokens':response["usage"]["total_tokens"],
        'response':response['choices'][0]['text']
    }

    # adicionando os dados no bd
    app.db.child("Output").child("Clean").push(data)
    #salvando o response completo da API tbm para nao perder nada
    app.db.child("Output").child("Raw").push(response)

    return answer
