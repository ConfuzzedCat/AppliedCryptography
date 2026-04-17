#!/usr/bin/env python

from socket import *
server_name = input("Enter your server's ip: ")
server_port = int(input("Enter your server's port: "))
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))

bCloseConnection = False

try:
    while not bCloseConnection:
        message = input("Please enter your message: ")
        client_socket.send(message.encode())
        modified_message = client_socket.recv(2048)
        print("From server: ", modified_message.decode())
        if message == "bye":
            bCloseConnection = True
except KeyboardInterrupt:
    client_socket.shutdown(SHUT_RDWR)
    client_socket.close()
