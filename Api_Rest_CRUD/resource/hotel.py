from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found'}, 404 # not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}'already exists.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        novo_hotel.save_hotel()
        return novo_hotel.json()




        #novo_hotel = novo_objeto.json()
        #novo_hotel = { 'hotel_id':hotel_id, **dados }
        #hoteis.append(novo_hotel)
        #return novo_hotel, 200




    def put(self, hotel_id):

         dados = Hotel.argumentos.parse_args()
         novo_objeto = HotelModel(hotel_id, **dados)
         novo_hotel = novo_objeto.json()
         hotel = Hotel.find_hotel(hotel_id)
         if hotel:
             hotel.update(novo_hotel)
             return novo_hotel, 200
         hoteis.append(novo_hotel)
         return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted. '}
