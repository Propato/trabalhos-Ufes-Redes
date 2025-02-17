from client import ClientConection

HOST = "127.0.0.1"
PORT = 8000

client = ClientConection(HOST, PORT)
client.start()
client.run()