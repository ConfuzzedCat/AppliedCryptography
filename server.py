#!/usr/bin/env python

from socket import *

IP = ''
PORT = 12001
server_port = PORT
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(1)
print(f"The server is ready to receive ({server_socket.getsockname()})")
try:
    while True:
        conn_socket,client_address = server_socket.accept()
        message = ""
        bCloseConnection = False
        while not bCloseConnection:
            message = conn_socket.recv(2048).decode()
            conn_socket.send(message.encode())
            print("connection received from {}, and {} is sent back".format(client_address[1], message))
            if message == "bye":
                bCloseConnection = True
        conn_socket.close()
except KeyboardInterrupt:
    print("\b\bClosing server")
finally:
    server_socket.close()
