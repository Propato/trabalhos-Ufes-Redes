import os
import json
import socket
from concurrent.futures import ThreadPoolExecutor

# import sys
# import signal

from ui import UI
from client import Client

class Server():
    def __init__(self, host, port, max_clients, free_teams):
        try:
            self.ui = UI(0)
            
            self.port = port
            self.host = host

            self._max_clients = max_clients
            self._clients = {}
            self.free_teams = free_teams
            self.teams = {} # Broadcast Server
            
            try:
                with open("./users.json", "r") as file:
                    self._data = json.load(file)
            except:
                self._data = {}
            
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((host, port))

            # signal.signal(signal.SIGINT, self.handle_shutdown)
            # signal.signal(signal.SIGTERM, self.handle_shutdown)

        except Exception as e:
            print(self.ui.format_msg("Error on Constructor Server", os.get_terminal_size().columns, color="red"))
            print(e)
            print()
            self.close()

    def run(self):
        try:
            self._socket.listen()
            print(self.ui.format_msg(f"Listening on {self.host}:{self.port}", os.get_terminal_size().columns, color="green"))

            # Create a thread pool with a maximum of 5 worker threads
            with ThreadPoolExecutor(max_workers=self._max_clients) as executor:
                while True:
                    # accept a client connection
                    client_socket, addr = self._socket.accept()
                    client = Client(self, client_socket, addr)

                    print(self.ui.format_msg(f"Client {addr[0]}:{addr[1]} Accepted", os.get_terminal_size().columns, color="green"))
                    # Submit the task to the thread pool
                    executor.submit(client.handle)
        except (EOFError, KeyboardInterrupt):
            print(self.ui.format_msg("Closing", os.get_terminal_size().columns, color="yellow"))
        except Exception as e:
            print(self.ui.format_msg("Error on Running Server", os.get_terminal_size().columns, color="red"))
            print(e)
        finally:
            self.close()

    def setClient(self, addr, client):
        self._clients[addr] = client

    def getClients(self):
        msg = "Addrs - Level: name"
        for client in self._clients.values():
            user = client._user if client._user else "Unknow"
            msg += f"{client.port} - {client._user_level}: {user}\n"
        return msg
    
    def getTeams(self, level):
        msg = "Team - Number of clients:\n"
        for name in self.teams:
            msg += f"{name} - {len(self.teams[name]['clients'])}\n"
            if level == 2:
                for client in self.teams[name]['clients']:
                    msg += f"\t{client}\n"
                
        return msg
    
    def delClient(self, addr):
        if self._clients[addr]:
            del self._clients[addr]
            return True
        print(self.self.ui.format_msg(f"Error on del Client {addr}", color="red"))
        return False
    
    def registerUser(self, user):
        self._data.update(user)
        with open('./users.json', 'w') as f:
            json.dump(self._data, f, indent=4)

    def close(self):
        try:
            for client in list(self._clients.values()):
                try:
                    client.close(0)
                except Exception as e:
                    print(self.ui.format_msg(f"Error on Close Client {client.host}:{client.port}", os.get_terminal_size().columns, color="red"))
                    print(e)
            
            for user in self._data.values():
                user['status'] = 0
            with open('./users.json', 'w') as f:
                json.dump(self._data, f, indent=4)

            if self._socket:
                self._socket.close()
                self._socket = None
                print(self.ui.format_msg("Server closed", os.get_terminal_size().columns, color="green"))
            else:
                print(self.ui.format_msg("Server alread closed", os.get_terminal_size().columns, color="yellow"))
        except Exception as e:
            print(self.ui.format_msg("Error on Close Server", os.get_terminal_size().columns, color="red"))
            print(e)

    # def handle_shutdown(self, signum, frame):
    #     print()
    #     print(self.ui.format_msg("Shutting down server...", os.get_terminal_size().columns, color="yellow"))
    #     sys.exit(0)
    