import threading
import socket
import pickle

HOST = "185.227.111.128" # '127.0.0.1' 
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(pickle.dumps(message))

def handle(client):
	while True:
		try:
			message = pickle.loads(client.recv(1024))
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast(f"{nickname} left the chat!")
			nicknames.remove(nickname)
			break

def receive():
	while True:
		client, address = server.accept()
		print(f"Connected with: {str(address)}")

		client.send(pickle.dumps("NICK"))
		nickname = pickle.loads(client.recv(1024))
		nicknames.append(nickname)
		clients.append(client)

		print(f"Nickname of the client is {nickname}!")
		broadcast(f"{nickname} joined the chat!")
		client.send(pickle.dumps("Connected to the server!"))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

print("Server is listening!")
receive()
