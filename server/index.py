from server import Server

HOST = "127.0.0.1"
PORT = 8000
MAX_CLIENTS = 5
FREE_TEAMS = 2

server = Server(HOST, PORT, MAX_CLIENTS, FREE_TEAMS)

server.run()