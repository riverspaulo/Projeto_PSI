
from flask import Flask, redirect, render_template, url_for, request, flash
from models import User, obter_conexao
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message

# 1 - Adicionar o LoginManager
from flask_login import LoginManager, login_user, login_required, logout_user
login_manager = LoginManager()

app = Flask(__name__)
# Config do flask-mail
app.config['MAIL_SERVER']= 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '3a0ea47949473c'
app.config['MAIL_PASSWORD'] = 'f529827f19de12'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# 2 - Configurar app para trabalhar junto com flask-login
login_manager.init_app(app)

# 3 - ncessário adicionar uma chave secreta para aplicaçãos
app.config['SECRET_KEY'] = 'ULTRAMEGADIFICIL'

# 4-  Função utilizada para carregar o usuário da sessão (logado)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():    
    return render_template('pages/index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha'] 
        msg = Message(subject='Olá caro leitor!', sender='peter@mailtrap.club', recipients=[email])
        msg.body = "Obrigado por acessar nosso site, cadastre-se para aproveitar!!!."
        mail.send(msg)
        if not User.exists(email):
            user = User(email=email, senha=senha)
            user.save()            
            # 6 - logar o usuário após cadatro
            login_user(user)
            flash("Cadastro realizado com sucesso")
            return redirect(url_for('login'))
    return render_template('pages/register.html')


# 7 - logar um usuário já existente
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']   
        user = User.get_by_email(email)

        if user and check_password_hash(user['senha'], senha):
            login_user(User.get(user['id']))
            flash("Você está logado")
            return redirect(url_for('recomend'))
        
        else:
            flash("Dados incorretos")
            return redirect(url_for('login'))
    return render_template('pages/login.html')
             
@app.route('/recomendação', methods=['POST', 'GET'])
def recomend():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        recomendacao = User(titulo=titulo, autor=autor)
        recomendacao.save_recomendacoes()
        flash("Recomendação enviada com sucesso")
        return redirect(url_for('rec_usuarios'))  
    return render_template('pages/recomend.html')

@app.route('/recomendações_usuarios')
def rec_usuarios():
    return render_template('pages/rec_usuarios.html', recomendacoes = User.all_recomendacoes(User))

@app.route('/cad_favoritos')
def favoritos():
    if request.method == 'POST':
       livro = request.form["livro"]
       escritor = request.form["escritor"]
       favorito = User(livro=livro, escritor=escritor)
       favorito.save_favoritos()
       flash("Livro adicionado aos favoritos")
       return redirect(url_for('dash'))
    return render_template('pages/cad_favoritos.html')

@app.route('/dashboard') #Página que exibe os favoritos 
@login_required
def dash():
    return render_template('pages/dash.html', favoritos = User.all_favoritos(User))

# 8 - logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
