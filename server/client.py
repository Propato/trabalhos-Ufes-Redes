import os
import sys

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

from ui import UI

class Client():
    def __init__(self, server, socket, addr):
        self._socket = socket
        self.host = addr[0]
        self.port = addr[1]
        
        self._user = None
        self._user_level = 0 

        self._private_key = None
        self._public_key = None
        
        self._session_key = None
        self._crypt = None
        
        self._server = server
        server.setClient(f"{self.host}:{self.port}", self)
        self.ui = UI(0)


    def handle(self):
        self.cripto()
        self.start() # Get terminal size & send Intro
        self.menu()

    def start(self):
        while True:
            self.write("Send your terminal width: ")
            request = self.read() # Get request

            try:
                self.ui.terminal_size = int(request)
                break
            except:
                self.ok("\033[31mInvalid terminal width. Please, fix and send again...\n\033[0m") # Bad request
                continue

        self.ok("Accepted")
        self.ok(self.ui.Intro()) # Shows the intro message

    def cripto(self):
        try:
            self._private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self._public_key = self._private_key.public_key()

            # Send public key
            public_pem = self._public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            self._socket.sendall(public_pem)

            # Get session_key
            session_key = self._socket.recv(1024)
            self._session_key = self._private_key.decrypt(
                session_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 é o algoritmo de máscara
                    algorithm=hashes.SHA256(),
                    label=None # Opcional, geralmente None
                )
            )
            self._crypt = Fernet(self._session_key)
            self._socket.sendall(self._crypt.encrypt(self._session_key))

            msg = self._socket.recv(1024).decode("utf-8")
            if msg != "Accepted":
                raise Exception("Session keys don't match") 
        except Exception as e:
            print(f"Error on Setting Session Key: {e}")
            self.close(1, False)

    def menu(self):
        while True:
            self.write(self.ui.Menu(self._user_level)) # Shows the menu

            request = self.read() # Get request
            print(f"{self.host}:{self.port} - {self._user or "Unknow"} > {request}")

            try:
                option = int(request)
                option = self.ui.getOption(self._user_level, option)

                print(f"{self.host}:{self.port} - {self._user or "Unknow"} > {option}")
            except:
                self.ok(self.ui.format_msg("Invalid option", None, "red")) # Bad request, try again
                print(f"{self.host}:{self.port} - {self._user or "Unknow"} > Invalid")
                print("Invalid\n")
                continue

            self.ok("Accepted")
            self.handle_options(option)
            print()


    def handle_options(self, option):
        if option == "Register":
            self.register()
        elif option == "Login":
            self.login()
        elif option == "Show teams":
            self.showTeams()
        elif option == "Join team":
            self.joinTeam()
        elif option == "Start team":
            self.startTeam()
        elif option == "Show online clients":
            self.showOnlineClients()
        elif option == "Logout":
            self.logout()
        elif option == "Close":
            self.close(0)
        # elif option == "Invalid":
        #     print("Invalid")
        else:
            print("Damn, how did u got here?")

    def register(self):
        self.write("User: ") # Ask for credentials
        user = self.read() # Get request

        if not user in self._server._data:
            self.ok("Accepted")

            self.write("Password: ") # Ask for password

            password = self.read().encode("utf-8") # Get request and encrypt
            passhash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            level = 1 if not self._user_level else 2
            self._server.registerUser({ user: {
                    "password": passhash,
                    "level": level,
                    "status": 0
                    }
                })

            self.ok(self.ui.format_msg(f"Registered: {user}", None, color="green"))
            return
        self.ok(self.ui.format_msg("Already registered User", None, color="red"))
        return

    def login(self):
        self.write("User: ") # Ask for credentials
        user = self.read() # Get request

        if user in self._server._data:
            self.ok("Accepted")
            self.write("Password: ") # Ask for password

            if bcrypt.checkpw(self.read().encode('utf-8'), self._server._data[user]["password"].encode('utf-8')): # Verify password

                if self._server._data[user]['level'] == 1 and self._server._data[user]['status']:
                    self.ok(self.ui.format_msg(f"user {user} is already logged in", None, color="red"))
                    self.close(0)
                
                self.ok(self.ui.format_msg(f"Authenticated: {user}", None, color="green"))

                self._user = user # Set User
                self._user_level = int(self._server._data[self._user]["level"])
                self._server._data[self._user]['status'] = 1
                return
            
            self.ok((self.ui.format_msg("Wrong Password", None, color="red")))
            return
        
        self.ok(self.ui.format_msg("Unknow User", None, color="red"))
    
    def showTeams(self):
        self.write(self._server.getTeams(self._user_level) + "\nSend any key to show menu... ")
        self.read()
        self.ok("Accepted")

    def joinTeam(self):
        # Get name
        self.write("Team name: ")
        name = self.read()

        # Join team
        if name in self._server.teams:
            if self._user in self._server.teams[name]['clients']:
                self.ok(self.ui.format_msg(f"You are already in the team", None, color="yellow"))
                return
            self.ok("Accepted")

            # Get password
            self.write("Team password: ")
            password = self.read()

            if password == self._server.teams[name]["password"]:
                self._server.teams[name]['clients'].append(self._user)
                self.ok(self.ui.format_msg(f"joined in {name}", None, color="green"))
                return

            self.ok(self.ui.format_msg(f"Wrong Password", None, color="red"))
            return
        
        self.ok(self.ui.format_msg(f"Team {name} doesn't exist", None, color="red"))
    
    def startTeam(self):
        if self._server.free_teams <= 0:
            self.write(self.ui.format_msg("No more teams available", None, color="red") + "\nSend any key to show menu... ")
            self.read()
            self.ok("Accepted")
            return

        # Get name
        self.write("Team name: ")
        name = self.read()

        # Create team
        if not name in self._server.teams:
            self.ok("Accepted")

            # Get password
            self.write("Team password: ")
            password = self.read()

            self._server.teams[name] = {
                    "password": password,
                    "clients": []
                }
            
            self._server.free_teams -= 1
            self.ok(self.ui.format_msg(f"Team {name} started", None, color="green"))

            return
        self.ok(self.ui.format_msg(f"Team {name} already exists", None, color="yellow"))
        

    def showOnlineClients(self):
        self.write(self._server.getClients() + "\nSend any key to show menu... ")
        self.read()
        self.ok("Accepted")
    
    def logout(self):
        self.write("Log Out? y/n") # Confirm
        request = self.read() # Get request

        if request.lower() in ['y', 'ye', 'es', 'ys', 'yes']:
            self.ok(self.ui.format_msg(f"Logged Out {self._user}", None, color="green"))

            # Reset Credentials
            self._server._data[self._user]['status'] = 0
            self._user = None # Reset User
            self._user_level = 0 # Reset Level
            return
            
        self.ok((self.ui.format_msg(f"Still Authenticated {self._user}", None, color="yellow")))
        return
    
    def read(self):
        if not self._socket:
            print("Error Read: Server not yet started")
            self.close(1)
        
        try:
            msg = self._socket.recv(1024) # Get message
            msg = self._crypt.decrypt(msg) # Decrypt by session key
            msg = self._private_key.decrypt( # Decrypt by private key
                msg,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 é o algoritmo de máscara
                    algorithm=hashes.SHA256(),
                    label=None # Opcional, geralmente None
                )
            ).decode("utf-8")
            # request = self._crypt.decrypt(self._socket.recv(1024).decode("utf-8")).decode("utf-8")
        except Exception as e:
            print(f"Error on reading: {e}")
            self.close(1, False)

        if not msg:
            self.close(1)
        if msg.lower() == "close":
            self.close(0)

        return msg
        
    def write(self, text):
        if not self._socket:
            print(f"Error Write {text}: Server not yet started")
            self.close(1)

        if not text or text == "":
            print("Invalid text")
            self.close(1)
        if len(text) > 1024:
            print("Maximum size reached (1024), cutting off text")
            # text = text[:1024]
        
        try:
            self._socket.sendall(self._crypt.encrypt(text.encode("utf-8"))[:1024])
        except Exception as e:
            print(f"Error on writing: {e}")
            self.close(1, False)

    def ok(self, msg, ok="Ok"):
        while True:
            self.write(msg)
            if self.read() == ok:
                break

    def close(self, status, writing=True):
        try:
            if self._server:
                if self._user:
                    self._server._data[self._user]['status'] = 0
                self._server.delClient(f"{self.host}:{self.port}")
                self._server == None

            if self._socket:
                if writing:
                    self.write("closed")
                self._socket.close()
                self._socket = None

                print(self.ui.format_msg(f"Client {self.host}:{self.port} closed", os.get_terminal_size().columns, color="green"))
            else:
                print(self.ui.format_msg(f"Client {self.host}:{self.port} alread closed", os.get_terminal_size().columns, color="yellow"))
        except Exception as e:
            print(self.ui.format_msg(f"Error on Close Client {self.host}:{self.port}", os.get_terminal_size().columns, color="red"))
            print(e)
        finally:
            sys.exit(status)