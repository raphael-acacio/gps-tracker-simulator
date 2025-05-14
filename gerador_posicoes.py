import random
import requests
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('OPENCAGE_API_KEY')

def gerar_coordenada_aleatoria():
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    return latitude, longitude

def buscar_endereco(latitude, longitude):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={API_KEY}&language=pt'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        endereco = data['results'][0]['formatted']
        return endereco
    return None

def inserir_posicao(latitude, longitude, endereco):
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()
        query = """
        INSERT INTO posicoes (latitude, longitude, endereco) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (latitude, longitude, endereco))
        conn.commit()
        print(f'Posição inserida: {latitude}, {longitude} - Endereço: {endereco}')
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no banco de dados: {err}")
    finally:
        cursor.close()
        conn.close()

latitude, longitude = gerar_coordenada_aleatoria()
endereco = buscar_endereco(latitude, longitude)

if endereco:
    inserir_posicao(latitude, longitude, endereco)
else:
    print("Não foi possível encontrar o endereço.")
