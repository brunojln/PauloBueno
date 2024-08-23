import socket
import random
import os
import hashlib
import datetime
import csv

class Client:
    def __init__(self):
        self.path = "/home/exati/Desktop/Client/"  # "C:\\Users\\Usuario\\Desktop\\teste\\cliente\\"

    def run(self):
        try:
            # Conecta ao servidor
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", 12000))

            # Pega os dados aleatórios
            selected_variables = self.get_random_values()
            selected_model_path = selected_variables["selectedModelPath"]
            selected_signal_path = selected_variables["selectedSignalPath"]
            signal_gain = int(selected_variables["signalGain"])
            selected_algorithm = selected_variables["selectedAlgorithm"]
            selected_model_flag = int(selected_variables["selectedModelFlag"])
            client_id = selected_variables["clientId"]

            # Cria o DataObject
            data_object = DataObject(
                selected_model_path, self.get_vector_data(selected_signal_path), selected_algorithm,
                selected_model_flag, client_id, selected_signal_path
            )

            # Envia o DataObject para o servidor
            print("Enviando objeto para o servidor")
            sock.sendall(pickle.dumps(data_object))

            # Recebe a resposta do servidor
            while True:
                result = sock.recv(1024).decode()
                if result == client_id:
                    name = sock.recv(1024).decode()
                    length = sock.recv(1024).decode()
                    hash_value = sock.recv(1024).decode()
                    iterations = sock.recv(1024).decode()
                    start = sock.recv(1024).decode()
                    end = sock.recv(1024).decode()

                    file_name = f"{client_id}_image.png"
                    self.receive_file(self.path + file_name, sock)
                    print(f"O arquivo {name} tem tamanho {length} bytes, tem a hash {hash_value} e a resposta foi {result}")

                    if self.sha(self.path + file_name) == hash_value:
                        print("Os hashes são iguais")

                    self.generate_report(
                        name, client_id, iterations, start, end, data_object.text, selected_model_flag
                    )
                    break
                elif result == "nok":
                    print(f"A resposta foi {result}, pois o arquivo requisitado não existe!")
                else:
                    print("Não recebeu")

        except Exception as e:
            raise RuntimeException(e)
        finally:
            sock.close()

    def get_random_values(self):
        # Implementar a lógica para gerar valores aleatórios
        pass

    def get_vector_data(self, file_path):
        # Implementar a lógica para obter os dados do arquivo
        pass

    def receive_file(self, file_name, sock):
        print(f"Iniciando ReceiveFile {file_name}")
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "wb") as f:
            size = int(sock.recv(1024).decode())
            print(size)
            while size > 0:
                data = sock.recv(4096)
                if not data:
                    break
                f.write(data)
                size -= len(data)
        print("Arquivo recebido")

    def sha(self, file_name):
        with open(file_name, "rb") as f:
            bytes = f.read()
            hash_object = hashlib.sha256(bytes)
            hex_hash = hash_object.hexdigest()
        return hex_hash

    def generate_report(self, name, client_id, iterations, start, end, algorithm_data, selected_model_flag):
        report_path = os.path.join(self.path, "Reports", f"report_{client_id}.txt")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, "w") as f:
            f.write(
                f"\nImagem: {name}\n"
                f"{algorithm_data}\n"
                f"Iterações: {iterations}\n"
                f"Hora de Início: {start}\n"
                f"Hora de Finalização: {end}"
            )
            if selected_model_flag == 1:
                f.write("\nPixels: 60x60")
            else:
                f.write("\nPixels: 30x30")

class DataObject:
    def __init__(self, model_path, signal, algorithm, model_flag, client_id, signal_path):
        self.model_path = model_path
        self.signal = signal
        self.algorithm = algorithm
        self.model_flag = model_flag
        self.client_id = client_id
        self.signal_path = signal_path
        self.text = f"Identificação do usuário: {client_id}\nIdentificação do algoritmo utilizado: {algorithm}"

if __name__ == "__main__":
    # Gera um número aleatório de instâncias de cliente (por exemplo, entre 1 e 5)
    num_clients = random.randint(1, 5)
    print(f"Número de clientes sorteados: {num_clients}")

    for _ in range(num_clients):
        # Cria uma nova instância de Cliente e executa o método run
        client = Client()
        client.run()

        # Gera um intervalo de tempo aleatório entre a criação de instâncias (por exemplo, entre 1 e 5 segundos)
        interval_in_seconds = random.randint(1, 5)
        print(f"Aguardando {interval_in_seconds} segundos antes de criar a próxima instância")
        time.sleep(interval_in_seconds)