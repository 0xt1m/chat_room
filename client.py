import socket
import threading
import pickle

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1234))

def receive():
	while True:
		try:
			message = pickle.loads(client.recv(1024))
			if message == "NICK":
				client.send(pickle.dumps(nickname))
			else:
				print(message)
		except:
			print("An error occurred!")
			client.close()
			break

def write():
	while True:
		message = f"{nickname}: {input('')}"
		client.send(pickle.dumps(message))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()