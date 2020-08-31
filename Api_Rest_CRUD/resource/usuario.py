from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask import make_response, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The fiel 'login' cannot be left blank.")
argumentos.add_argument('senha', type=str, required=True, help="The fiel 'senha' cannot be left blank.")
argumentos.add_argument('email', type=str)
argumentos.add_argument('ativado', type=bool)

class User(Resource):
    #/Usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 # not found

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
                user.delete_user()
                return {'message': 'User deleted. '}
        return {'message': 'User not found. '}, 404

class UserRegister(Resource):
    #/cadastro
    def post(self):
        dados = argumentos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return{"messege": "The field 'email' cannot be left blank"},400

        if UserModel.find_by_email(dados['email']):
            return{"messege": "The email {} already existis".format(dados['email'])},400

        if UserModel.find_by_login(dados['login']):
            return{"messege": "The login '{}' already existis.".format(dados['login'])}, 400
        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return{'messege': 'An internal server erro has ocurred.'}, 500
        return{'messege': 'User created successfully!'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = argumentos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']): #confere se a senha passada por POST é igual a senha do banco de forma segura
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access token': token_de_acesso}, 200
            return{'messege': 'User not confirmed.'}, 400 #Unauthorized
        return{'messege': 'The user name or password is incorrect.'}, 401 #Unauthorized

class UserLogout(Resource):
    @jwt_required
    def post(cls):
        jwt_id = get_raw_jwt()['jti'] #JWT token indentifier
        BLACKLIST.add(jwt_id)
        return {'messege': 'logged out successfully!'}, 200

class UserConfirm(Resource):
    #raiz_do_site/confirmacao/user{id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return{"messege" : "User id '{}' not found".format(user_id)}, 404
        user.ativado = True
        user.save_user()
        #return{"messege": "User id '{}' confirmed successfully.".format(user_id)}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, usuario= user.login),200)
