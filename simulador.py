import socket
import mysql.connector
import requests
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def obter_endereco(lat, lon):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]['formatted']
    else:
        return "Endereço não encontrado"

def inserir_posicao(id_rastreador, lat, lon, spd, endereco):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """INSERT INTO posicoes (id, latitude, longitude, speed, ignition, endereco, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, NOW())"""
        cursor.execute(query, (id_rastreador, lat, lon, spd, endereco))
        conn.commit()
        print(f"Posição inserida: {id_rastreador}, {lat}, {lon}, {endereco}")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no banco: {err}")
    finally:
        cursor.close()
        conn.close()

def processar_string(mensagem):
    # Quebra a mensagem recebida e pega os dados
    dados = mensagem.strip().split(";")
    id_rastreador = dados[0].split(":")[1]
    lat = float(dados[1].split(":")[1])
    lon = float(dados[2].split(":")[1])
    spd = int(dados[3].split(":")[1])
    evt = dados[4].split(":")[1]

    endereco = obter_endereco(lat, lon)
    inserir_posicao(id_rastreador, lat, lon, spd, endereco)

    print(f"ID Rastreador: {id_rastreador}")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
    print(f"Velocidade: {spd} km/h")
    print(f"Endereço: {endereco}")

def iniciar_servidor():
    HOST = '127.0.0.1'
    PORT = 9000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Servidor escutando na porta {PORT}...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Conexão recebida de {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    mensagem = data.decode()
                    print(f"Recebido: {mensagem}")
                    processar_string(mensagem)
                    conn.sendall('Posição recebida e processada\n'.encode('utf-8'))

if __name__ == "__main__":
    iniciar_servidor()
