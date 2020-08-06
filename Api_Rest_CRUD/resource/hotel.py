from flask_restful import Resource

hoteis = [
        {
        'hotel_id': 'alpha',
        'nome:': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria':420.34,
        'cidade':'Rio de Janeiro'
        },
        {
        'hotel_id': 'bravo',
        'nome:': 'Bravo Hotel',
        'estrelas': 5.0,
        'diaria':5000,
        'cidade':'Niteroi'
        },
        {
        'hotel_id': 'charlie',
        'nome:': 'Charlie Hotel',
        'estrelas': 4.4,
        'diaria':380.34,
        'cidade':'Santa Catarina'
        }
        ]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}
