import sqlite3
#Apenas um exemplo de como criar manualmente, porém estamos utilizando

connection = sqlite3.connect('banco.db')
cursor = connection.cursor() #cursor é o que ira selecionar as informações no banco de dados

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, nome text, estrelas real, diaria real, cidade text)"

cria_hotel = "INSERT INTO hoteis VALUES('alpha', 'Hotel Alpha', 4.3, 250.10, 'Rio de Janeiro')"



cursor.execute(cria_tabela)
cursor.execute(cria_hotel)


connection.commit()
connection.close()
