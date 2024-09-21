from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('pages/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('pages/register.html')

@app.route('/recomendação')
def recomend():
    return render_template('pages/recomend.html')
