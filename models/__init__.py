from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector


def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_livros"
    )   


class User(UserMixin):
    _hash : str
    def __init__(self, **kwargs):
        self._id = None
        if 'email' in kwargs.keys():
            self._email = kwargs['email']
        if 'senha' in kwargs.keys():
            self._senha = kwargs['senha']
        if 'hash' in kwargs.keys():
            self._hash = kwargs['hash']
        if 'titulo' in kwargs.keys():
            self._titulo = kwargs['titulo']
        if 'autor' in kwargs.keys():
            self._autor = kwargs['autor']
        if 'livro' in kwargs.keys():
            self._livro = kwargs['livro']
        if 'escritor' in kwargs.keys():
            self._escritor = kwargs['escritor']


    def get_id(self):
        return str(self._id)

    
    @property
    def _senha(self):
        return self._hash
    
    @_senha.setter
    def _senha(self, senha):
        self._hash = generate_password_hash(senha)

    
    def save(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO users(email, senha) VALUES (%s, %s)", (self._email, self._hash,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True
    
    def save_recomendacoes(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO recomendacoes(titulo, autor) VALUES (%s, %s)", (self._titulo, self._autor,))
        conn.commit()
        conn.close()
        return True
    
    def all_recomendacoes(cls):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT titulo, autor FROM recomendacoes")
        recomendacoes = cursor.fetchall()
        conn.commit()
        conn.close()
        return recomendacoes
    
     
    def save_favoritos(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO favoritos(livro, escritor) VALUES (%s, %s)", (self._livro, self._escritor,))
        conn.commit()
        conn.close()
        return True
    
    def all_favoritos(cls):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT livro, escritor FROM favoritos")
        favoritos = cursor.fetchall()
        conn.commit()
        conn.close()
        return favoritos
    
    @classmethod
    def get(cls,user_id):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user:
            loaduser = User(email=user['email'] , hash=user['senha'])
            loaduser._id = user['id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, email):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        if user:
            return True
        else:
            return False
    
    
    
    @classmethod
    def get_by_email(cls,email):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT id, email, senha FROM users WHERE email = %s", (email,))
        user = cursor.fetchone() 
        conn.commit()
        conn.close()
    
        return user
