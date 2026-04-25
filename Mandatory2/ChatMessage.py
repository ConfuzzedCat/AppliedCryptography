import json
import base64
class ChatMessage:
    nonce: bytes
    aad: bytes
    cipher_text: bytes

    def __init__(self, nonce: bytes, aad: bytes, cipher_text: bytes):
        self.nonce = nonce
        self.aad = aad
        self.cipher_text = cipher_text


def chat_message_encode(chat_msg: ChatMessage)-> bytes:
    nonce_str = base64.b64encode(chat_msg.nonce).decode()
    aad_str = base64.b64encode(chat_msg.aad).decode()
    cipher_text_str = base64.b64encode(chat_msg.cipher_text).decode()
    json_dump = json.dumps({"nonce": nonce_str, "aad": aad_str, "cipher_text": cipher_text_str})
    return json_dump.encode()

def chat_message_decode(encoded_msg: bytes) -> ChatMessage:
    msg = json.loads(encoded_msg.decode())
    nonce_bytes = base64.b64decode(msg["nonce"])
    aad_bytes = base64.b64decode(msg["aad"])
    cipher_text_bytes = base64.b64decode(msg["cipher_text"])
    return ChatMessage(nonce_bytes, aad_bytes, cipher_text_bytes)
