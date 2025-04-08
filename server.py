import socket
import threading
import time

class SensorServer:
    def __init__(self, host='localhost', port=6000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.sensor_data = {}
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Servidor iniciado na porta {self.port}...")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexão de {addr} estabelecida")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            with client_socket:
                
                sensor_id = client_socket.recv(1024).decode().strip()
                if not sensor_id:
                    print("ID do sensor não recebido")
                    return
                
                with self.lock:
                    self.sensor_data[sensor_id] = "Nenhum dado"
                self.display_status()
                
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                    parts = data.split(':')
                    if len(parts) != 2:
                        continue
                    sensor_id_received, value = parts[0], parts[1]
                    
                    with self.lock:
                        self.sensor_data[sensor_id_received] = value
                    self.display_status()
                    
        except Exception as e:
            print(f"Erro ao tratar cliente: {e}")
        finally:
            with self.lock:
                if sensor_id in self.sensor_data:
                    del self.sensor_data[sensor_id]
            self.display_status()

    def display_status(self):
        with self.lock:
            print("\nEstado atual dos sensores:")
            for sensor, value in self.sensor_data.items():
                print(f"{sensor}: {value}")
            print()

if __name__ == "__main__":
    server = SensorServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado")
