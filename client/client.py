import os
import sys
import socket

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

class ClientConection():
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket = None
        
        self._public_key = None
        self._session_key = Fernet.generate_key()[:1024]
        self._crypt = Fernet(self._session_key)

    def run(self):
        self.intro()
        self.menu()

    def start(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
            self._socket.connect((self._host, self._port)) # Establish connection with server
        except Exception as e:
            print(f"Error on starting: {e}")
            self.close(1)

        self.cripto()

        while True:
            self.read() # Read initial message
            if not self.write(f"{os.get_terminal_size().columns}"): # Send terminal size
                self.close(1)
            if self.ok():
                break

    def cripto(self):
        key = None
        try:
            public_pem = self._socket.recv(1024) # Get public key
            self._public_key = serialization.load_pem_public_key(public_pem) # Set public key

            encrypted_session_key = self._public_key.encrypt(
                self._session_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 é o algoritmo de máscara
                    algorithm=hashes.SHA256(),
                    label=None # Opcional, geralmente None
                )
            ) # Encrypted session key with public key

            self._socket.sendall(encrypted_session_key)
            key = self._crypt.decrypt(self._socket.recv(1024))
            
            if self._session_key != key:
                self._socket.sendall("Session keys don't match".encode("utf-8"))
                raise Exception("Session keys don't match") 
            self._socket.sendall("Accepted".encode("utf-8"))
        except Exception as e:
            print(f"Error Setting Keys: {e}")
            self.close(1)

    def intro(self):
        print(self.read())
        self.write("Ok")

    def menu(self):
        while True:
            print(self.read())
            while not self.write(input("< ")):
                continue
            self.ok()
        
    def read(self):
        if not self._socket:
            print("Server not yet started")
            sys.exit(1)
        
        try:
            response = self._crypt.decrypt(self._socket.recv(1024).decode("utf-8")).decode("utf-8")
        except Exception as e:
            print(f"Error on reading: {e}")
            self.close(1)

        if not response:
            self.close(1)
        if response.lower() == "closed":
            self.close(0)
        return response
        
    def write(self, text):
        if not self._socket:
            print(f"Error Write {text}: Server not yet started")
            self.close(1)
        
        if not text or text == "":
            print("Invalid text")
            return False
        if len(text) > 190:
            print("Maximum size reached (190)")
            return False
        
        try:
            # Criptografia com base na chave publica
            text = self._public_key.encrypt(
                    text.encode("utf-8"),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 é o algoritmo de máscara
                        algorithm=hashes.SHA256(),
                        label=None # Opcional, geralmente None
                    )
                )
            
            text = self._crypt.encrypt(text)
            
            if len(text) > 1024:
                # print("Maximum size reached (1024), cutting off text")
                print("Maximum size reached (1024)")
                text = text[:1024]
                print("Vai dar ruim, manda outra coisa") # Se a mensagem criptografada passar de 1024, quando descriptografar, tera inconsistencia
                return False
        
            self._socket.sendall(text)
            return True
        except Exception as e:
            print(f"Error on writing: {e}")
            self.close(1)
        
    def ok(self, accepted="Accepted", ok="Ok"):
        request = self.read()
        if request != accepted:
            print(request)

        self.write(ok)
        return request == accepted
        
    def close(self, status):
        print("> closed")
        
        if not self._socket:
            print("Server already closed")
            return
        
        try:
            self._socket.close()
            self._socket = None
            print("Connection to server closed")
        except Exception as e:
            print(f"Error on closing conection: {e}")
        finally:
            sys.exit(status)
