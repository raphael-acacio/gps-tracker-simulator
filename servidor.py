import socket
from parser import analisar_mensagem

HOST = '0.0.0.0'
PORT = 9000

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Conexão de {addr}")

            with conn:
                buffer = ""
                while True:
                    dados = conn.recv(1024)
                    if not dados:
                        break

                    buffer += dados.decode()

                    # trata múltiplas mensagens
                    while "\n" in buffer:
                        linha, buffer = buffer.split("\n", 1)
                        resultado = analisar_mensagem(linha)
                        print("Recebido:", resultado)

if __name__ == "__main__":
    iniciar_servidor()
