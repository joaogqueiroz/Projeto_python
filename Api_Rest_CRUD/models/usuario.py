from sql_alchemy import banco
from flask import request, url_for
from requests import post
from properties import MAILGUN_DOMAIN, MAILGUN_API_KEY,FROM_TITLE,FROM_EMAIL

#Pegar as credenciais no Mailgun

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True) #SQL achemy entende que essa variavel por ser inteira e PK é um ID e assim a incrementa automaticamente
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email,ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
             }

    def send_confirmation_email(self):
        #[:-1] Pega do inicio da string -1
        #[:-1] Get  the start of string -1
        link = request.url_root[:-1]+url_for('userconfirm',user_id=self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
		             auth=('api', MAILGUN_API_KEY),
		             data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                           'to': self.email,
                           'subject': 'Confirmação de Cadastro',
                           'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                           'html': '<html><p>\
                           Confirme seu cadastro clicando no link a seguir: <a href="{}"> CONFIRMAR EMAIL</a>\
                           </p></html>'.format(link)
                           }
                    )


    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() #SELECT * FROM hotel_id = $hotel_id
        user = cls.query.filter_by(user_id=user_id).first() #SELECT * FROM user_id = $user_id
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first() #SELECT * FROM hotel_id = $hotel_id
        user = cls.query.filter_by(login=login).first() #SELECT * FROM login = $login
        if user:
            return user
        return None


    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first() #SELECT * FROM email = $email
        if user:
            return user
        return None
