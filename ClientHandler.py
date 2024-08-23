import socket
import os
import time
import hashlib
from datetime import datetime
from threading import Thread
from dataclasses import dataclass
import pickle
import csv

from algorithms.cgne import CGNE
from algorithms.cgnr import CGNR
from image import Image
from utils import get_matrix_data, get_vector_data

@dataclass
class DataObject:
    model_path: str
    h_path: str
    g: DoubleMatrix
    selected_algorithm: str
    selected_model_flag: int
    client_id: str
    signal_path: str
    text: str

class ClientHandler(Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.data_output_stream = client_socket.makefile('wb')
        self.so = SystemResourceObserver()
        self.path = "/home/exati/Desktop/Server/"  # "C:\\Users\\Usuario\\Desktop\\teste\\servidor\\"

    def run(self):
        try:
            while True:
                try:
                    data_object = pickle.load(self.client_socket.makefile('rb'))

                    if self.so.get_continue_ss(data_object.selected_model_flag):
                        print(self.data_output_stream)
                        print(f"Data: {data_object.text}")

                        if data_object.selected_algorithm == "CGNE":
                            try:
                                h = DoubleMatrix(get_matrix_data(data_object.h_path))
                                start = datetime.now()
                                print(f"CGNE is running! ClientId: {data_object.client_id}")
                                f = CGNE().get_image(h, data_object.g, data_object.selected_model_flag)
                                print(f"CGNE finalized! ClientId: {data_object.client_id}\n")
                                end = datetime.now()

                                file_name = f"{data_object.client_id}_image.png"
                                img = Image(f)
                                file = img.save_image(self.path, file_name)

                                if file.exists():
                                    self.client_socket.send(data_object.client_id.encode())
                                    hash_value = self.sha(file)
                                    file_size = os.path.getsize(file)
                                    iterations = CGNE.iterations

                                    self.client_socket.send(file_name.encode())
                                    self.client_socket.send(str(file_size).encode())
                                    self.client_socket.send(hash_value.encode())
                                    self.client_socket.send(str(iterations).encode())
                                    self.client_socket.send(start.strftime("%H:%M:%S").encode())
                                    self.client_socket.send(end.strftime("%H:%M:%S").encode())

                                    self.send_file(self.path + file_name, self.data_output_stream)
                                    time.sleep(0.5)
                                else:
                                    self.client_socket.send("nok".encode())
                            except (IOException, CsvException) as e:
                                raise RuntimeException(e)
                        elif data_object.selected_algorithm == "CGNR":
                            try:
                                h = DoubleMatrix(get_matrix_data(data_object.h_path))
                                start = datetime.now()
                                print(f"CGNR is running! ClientId: {data_object.client_id}")
                                f = CGNR().get_image(h, data_object.g, data_object.selected_model_flag)
                                print(f"CGNR finalized! ClientId: {data_object.client_id}\n")
                                end = datetime.now()

                                file_name = f"{data_object.client_id}_image.png"
                                img = Image(f)
                                file = img.save_image(self.path, file_name)
                                if file.exists():
                                    self.client_socket.send(data_object.client_id.encode())
                                    hash_value = self.sha(file)
                                    file_size = os.path.getsize(file)
                                    iterations = CGNR.iterations

                                    self.client_socket.send(file_name.encode())
                                    self.client_socket.send(str(file_size).encode())
                                    self.client_socket.send(hash_value.encode())
                                    self.client_socket.send(str(iterations).encode())
                                    self.client_socket.send(start.strftime("%H:%M:%S").encode())
                                    self.client_socket.send(end.strftime("%H:%M:%S").encode())

                                    self.send_file(self.path + file_name, self.data_output_stream)
                                else:
                                    self.client_socket.send("nok".encode())
                                print(f"Aqui foi {data_object.client_id}")
                            except (IOException, CsvException) as e:
                                raise RuntimeException(e)
                    else:
                        print("Não continua")
                except EOFError:
                    break
        except Exception as e:
            print(e)
            raise RuntimeException(e)
        finally:
            try:
                print("Entering try-catch")
                if self.data_output_stream is not None:
                    self.data_output_stream.close()
                    print("Closing dataOutputStream")
                self.client_socket.close()
                print("Closing socket")
            except IOException as e:
                print("Error")

    def send_file(self, path, data_output_stream):
        try:
            print("Iniciando sendFile")
            with open(path, "rb") as file:
                data_output_stream.write(str(os.path.getsize(path)).encode())
                data_output_stream.flush()

                buffer = file.read(4096)
                while buffer:
                    data_output_stream.write(buffer)
                    data_output_stream.flush()
                    buffer = file.read(4096)

            print("Arquivo enviado")
        except socket.error as e:
            print("Socket error")

    def sha(self, file):
        with open(file, "rb") as f:
            bytes = f.read()
            hash_object = hashlib.sha256(bytes)
            hex_hash = hash_object.hexdigest()
        return hex_hash

class SystemResourceObserver:
    def get_continue_ss(self, selected_model_flag):
        # Implement the logic to check if the system should continue processing
        return True

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12000))
    server_socket.listen(5)

    while True:
        print("Waiting for a connection")
        client_socket, address = server_socket.accept()
        print(f"Got connection from {address}")
        client_handler = ClientHandler(client_socket)
        client_handler.start()