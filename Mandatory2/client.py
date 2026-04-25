#!/usr/bin/env python

from socket import *
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from ChatMessage import *

def send_key_udp(ip: str, port: int, key: bytes):
    key_hash = hashlib.sha256(key).digest()
    udp_client_socket = socket(AF_INET, SOCK_DGRAM)
    udp_client_socket.sendto(key, (ip, port))
    modified_message, server_address = udp_client_socket.recvfrom(2048)
    if modified_message != key_hash:
        print("Wrong hash for key.")
        exit(1)
    udp_client_socket.close()

def send_message(client: socket, message: str, aes: AESGCM, nonce: bytes, aad: bytes):
    encrypted_message = aes.encrypt(nonce= nonce, data=message.encode(), associated_data=aad)
    msg = ChatMessage(nonce, aad, encrypted_message)
    encoded_message = chat_message_encode(msg)
    client.send(encoded_message)

def receive_message(data: bytes, aes: AESGCM) -> str:
    data = chat_message_decode(data)
    return aes.decrypt(nonce=data.nonce, data=data.cipher_text, associated_data=data.aad).decode()

key = AESGCM.generate_key(bit_length=128)
cipher = AESGCM(key)
server_name = input("Enter your server's ip: ")
server_port = int(input("Enter your server's port: "))
associated_data = b'This is a verified message by me.'
send_key_udp(server_name, server_port, key)
input("Press any key to continue...")
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))
bCloseConnection = False

try:
    while not bCloseConnection:
        message = input("Please enter your message: ")
        rand_nonce = os.urandom(12)
        send_message(client_socket, message, cipher, rand_nonce, associated_data)
        recv_data = client_socket.recv(2048)
        server_message = receive_message(recv_data, cipher)

        print("From server: ", server_message)
        if message == "bye" or message == "exit":
            bCloseConnection = True
except KeyboardInterrupt:
    client_socket.shutdown(SHUT_RDWR)
    client_socket.close()