def encrypt(plaintext: str, keyword: str) -> str:
    keyword = (keyword * ((len(plaintext) // len(keyword)) + 1))[:len(plaintext)]
    ciphertext = ''.join(chr((ord(p) ^ ord(k)) % 256) for p, k in zip(plaintext, keyword))
    return ciphertext


def decrypt(ciphertext: str, keyword: str) -> str:
    return encrypt(ciphertext, keyword)
