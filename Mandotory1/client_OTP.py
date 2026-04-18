#!/usr/bin/env python

from socket import *
import OTP


server_name = input("Enter your server's ip: ")
server_port = int(input("Enter your server's port: "))
enc_key = ""
try:
    with open("key.txt") as f:
        enc_key = f.read()
except FileNotFoundError:
    enc_key = input("Enter your encryption key: ")
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))
bCloseConnection = False

try:
    while not bCloseConnection:
        message = input("Please enter your message: ")
        enc_message = OTP.encrypt(message, enc_key)
        client_socket.send(enc_message.encode())
        server_message = OTP.decrypt(client_socket.recv(2048).decode(), enc_key)

        print("From server: ", server_message)
        if message == "bye":
            bCloseConnection = True
except Exception as e:
    if type(e) != KeyboardInterrupt:
        print(e)
    client_socket.send("bye".encode())
    client_socket.shutdown(SHUT_RDWR)
    client_socket.close()
