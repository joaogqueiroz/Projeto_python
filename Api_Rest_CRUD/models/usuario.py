from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True) #SQL achemy entende que essa variavel por ser inteira e PK é um ID e assim a incrementa automaticamente
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, ativado):
        self.login = login
        self.senha = senha
        self.ativado = ativado

    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login,
            'ativado': self.ativado
             }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() #SELECT * FROM hotel_id = $hotel_id
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first() #SELECT * FROM hotel_id = $hotel_id
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
