from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pyrebase
import config
import aicontent

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.config.from_object(config.config['development'])
app.register_error_handler(404, page_not_found)

# initialize firebase
firebase = pyrebase.initialize_app(config.firebaseConfig)
# initialize auth e real time database
auth = firebase.auth()
db = firebase.database()

# Set the database rules using the Firebase Realtime Database console


app.secretkey = config.cookiesKey


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', **locals())

@app.route('/home', methods=["GET"])
def home():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('home.html', **locals())
    return redirect(url_for('login'))

@app.route('/newhome', methods=["GET"])
def newhome():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('new_home.html', **locals())
    return redirect(url_for('login'))


@app.route('/user', methods=["GET"])
def user():
    # get current user id making the request
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('user.html', **locals())
    return redirect(url_for('login'))


    

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return redirect(url_for('home'))
    if request.method == 'POST':
        # Get email and password from form
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        # Try to create an account
        try:
            #signup in firebase
            user = auth.create_user_with_email_and_password(email, password)
            #send email verification
            auth.send_email_verification(user['idToken'])
            #signup created with success, but still need to verify account
            signup_verify = True
            #saving data to send to db
            data = {
                'name':name,
                'email':email,
                'user_id':user['localId']
            }

            #refresh token
            # user = auth.refresh(session['refresh'])
            # session['refresh'] = user['refreshToken']
            
            #send data to db
            db.child("Users").push(data)
        except:
            signup_fail = 'Falha ao se cadastrar. Verifique se sua senha possui no mínimo 6 caracteres'
            return render_template('signup.html', **locals())
    return render_template('signup.html', **locals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return redirect(url_for('home'))
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')
        # Try to authenticate the user
        try:
            #login no firebase
            user = auth.sign_in_with_email_and_password(email, password)
            # Check if the user's email is verified
            info = auth.get_account_info(user['idToken'])
            if info['users'][0]['emailVerified'] == True:

                #cria uma session com esse token
                user_id = user['idToken']
                session['usr'] = user_id
                session['refresh'] = user['refreshToken']
                # print(user)
            # If the email is verified, redirect to the index page
                return redirect(url_for('home'))
            else:
            # If the email is not verified, render the login template with an error message
                message = 'Confirme seu cadastro no email antes de fazer login'
                return render_template('login.html', **locals())
        except:
            message = "Usuario não encontrado ou senha incorreta!"
            return render_template("login.html", **locals())
    # If the request is a GET request, render the login template
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usr')
    return redirect('/')


@app.route('/product-description', methods=["GET"])
def productDescription():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('product-description.html', **locals())
    return redirect(url_for('login'))


@app.route('/create-ads', methods=["GET"])
def createAds():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('create-ads.html', **locals())
    return redirect(url_for('login'))

@app.route('/email-marketing', methods=["GET"])
def emailMarketing():
    if ('usr' in session) and bool(auth.get_account_info(session['usr'])):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('email-marketing.html', **locals())
    session.clear()
    return redirect(url_for('login'))

@app.route('/posts', methods=["GET", "POST"])
def posts():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('posts.html', **locals())
    return redirect(url_for('login'))

@app.route('/post-ideas', methods=["GET", "POST"])
def postIdeas():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('post-ideas.html', **locals())
    return redirect(url_for('login'))

@app.route('/blog', methods=["GET", "POST"])
def blog():
    if ('usr' in session) and bool(auth.get_account_info(session['usr'])):
        #refresh token4
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('blog.html', **locals())
    session.clear()
    return redirect(url_for('login'))

# @app.route('/billing', methods=["GET"])
# def billing():
#     if ('usr' in session):
#         #refresh token
#         user = auth.refresh(session['refresh'])
#         session['refresh'] = user['refreshToken']

#         return render_template('billing.html', **locals())
#     return redirect(url_for('login'))

@app.route('/persona', methods=["GET"])
def persona():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        return render_template('persona.html', **locals())
    return redirect(url_for('login'))

@app.route('/airequest', methods=["POST"])
def aiRequest():
    request_data = request.get_json()
    input = request_data['input']
    category = request_data['category']
    openAIAnswer = aicontent.runAi(input, category)
    return jsonify(openAIAnswer)
    

# Pegar informações de usuário pra colocar na página de utilização

@app.route('/userinfo', methods=["GET"])
def userInfo():
    if ('usr' in session):
        #refresh token
        user = auth.refresh(session['refresh'])
        session['refresh'] = user['refreshToken']

        user =  auth.get_account_info(session['usr'])
        email = user['users'][0]['email']
        id_token = user['users'][0]['localId']
        result = db.child("Output").child("Clean").get()
        posts = []
        for res in result.each():
            posts.append(res.val())
        
        total_sum_tokens = 0
        for post in posts:
            try:
                if post['user_id_token'] == id_token:
                    total_tokens = post['total_tokens']
                    total_sum_tokens += total_tokens
            except KeyError:
                continue
        
        # precificacao
        preco_cem_tokens = 0.05 #centavos de real
        preco_cem_tokens_formatado = "R$ {:,.2f}".format(preco_cem_tokens)
        tokens_por_cem = total_sum_tokens/100 
        preco_final = tokens_por_cem * preco_cem_tokens
        preco_final_arredondado = round(preco_final,2)
        valor_utilizacao = "R$ {:,.2f}".format(preco_final_arredondado)
        mensalidade = 29
        valor_total = mensalidade + preco_final_arredondado
        valor_utilizacao_formatado = "R$ {:,.2f}".format(valor_total)
        data = {
            "email": email,
            "total_sum_tokens": total_sum_tokens,
            "preco_cem_tokens_formatado":preco_cem_tokens_formatado,
            "valor_utilizacao":valor_utilizacao,
            "mensalidade":mensalidade,
            "valor_utilizacao_formatado":valor_utilizacao_formatado
        }

        return jsonify(data)

    return redirect(url_for('login'))

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
