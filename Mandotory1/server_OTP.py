#!/usr/bin/env python

from socket import *
import OTP


IP = ''
PORT = 12002

KEY = ''
KEY_FILE = 'key.txt'

# Get or generate key
bSaveKey = False
with (open(KEY_FILE) as f):
    key_temp = f.readline().strip()
    if key_temp == "":
        bSaveKey = True
        key_temp = input("Enter key to be used for encryption: ")
    KEY = key_temp

if bSaveKey:
    with open(KEY_FILE, "w") as f:
        f.write(KEY)

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
            recv_msg = conn_socket.recv(2048).decode()
            message = OTP.decrypt(recv_msg, KEY)
            conn_socket.send(OTP.encrypt("From client: " + message, KEY).encode())
            print("connection received from {}, and '{}' is sent back".format(client_address[1], message))
            if recv_msg == "bye" or message == "bye":
                bCloseConnection = True
        conn_socket.close()
except KeyboardInterrupt:
    print("\b\bClosing server")
finally:
    server_socket.close()
