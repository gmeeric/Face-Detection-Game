import socket

HOST = "127.0.0.1"  # Localhost
PORT = 6000  # Port number

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(b"hello from client")
client.close()