import socket
import random
import time

class SensorClient:
    def __init__(self, host='localhost', port=6000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self.socket

    def send_data(self, socket):
        try:
            sensor_id = input("Digite o ID do sensor: ")
            socket.sendall(sensor_id.encode() + b'\n')

            while True:
                temp = 20.0 + random.uniform(0, 20)
                message = f"{sensor_id}:{temp:.1f}\n".encode()
                socket.sendall(message)
                print(f"Enviado: {message.decode().strip()}")
                time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
        finally:
            if socket:
                socket.close()

if __name__ == "__main__":
    client = SensorClient()
    try:
        socket = client.connect()
        client.send_data(socket)
    except Exception as e:
        print(f"Erro: {e}")
