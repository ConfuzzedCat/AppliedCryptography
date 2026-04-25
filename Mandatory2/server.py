#!/usr/bin/env python

import os
from socket import *
from ChatMessage import *
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib


# Functions
def send_message(server: socket, message: str, aes: AESGCM, nonce: bytes, aad: bytes):
    encrypted_message = aes.encrypt(nonce= nonce, data=message.encode(), associated_data=aad)
    msg = ChatMessage(nonce, aad, encrypted_message)
    encoded_message = chat_message_encode(msg)
    server.send(encoded_message)

def receive_message(data: bytes, aes: AESGCM) -> str:
    data = chat_message_decode(data)
    return aes.decrypt(nonce=data.nonce, data=data.cipher_text, associated_data=data.aad).decode()

# Constants
KEY_BITS = 128
BYTE_LEN = 8
KEY_BYTES_LENGTH = KEY_BITS/BYTE_LEN
NONCE_LEN = 12
SERVER_IP = "0.0.0.0"
SERVER_PORT = 12002
ASSOCIATED_DATA = b'Server Authenticity Data'
# UDP key server
key_server_socket = socket(AF_INET, SOCK_DGRAM)
key_server_socket.bind((SERVER_IP, SERVER_PORT))
print("The server is ready to receive the key")
key = b'\x00'
try:
    message,client_address = key_server_socket.recvfrom(2048)
    key = message
    key_hash = hashlib.sha256(key)
    key_server_socket.sendto(key_hash.digest(), client_address)
    print(f"Got key: sha256({key_hash.hexdigest()})")
except Exception as e:
    if type(e) == KeyboardInterrupt:
        exit("Exiting server")
    else:
        exit(e.args[0])
finally:
    key_server_socket.close()

if len(key) != KEY_BYTES_LENGTH:
    exit("Invalid key. Exiting server")

cipher = AESGCM(key)
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)
print(f"The server is ready to receive ({server_socket.getsockname()})")
try:
    while True:
        conn_socket,client_address = server_socket.accept()
        message = ""
        bCloseConnection = False
        while not bCloseConnection:
            recv_data = conn_socket.recv(2048)
            message = receive_message(recv_data, cipher)
            rand_nonce = os.urandom(NONCE_LEN)
            send_message(conn_socket,f"From client: {message}",cipher,rand_nonce,ASSOCIATED_DATA)
            print("connection received from {}, and '{}' is sent back".format(client_address[1], message))
            if message == "bye" or message == "exit":
                bCloseConnection = True
        conn_socket.close()
except KeyboardInterrupt:
    print("\b\bClosing server")
finally:
    server_socket.close()
