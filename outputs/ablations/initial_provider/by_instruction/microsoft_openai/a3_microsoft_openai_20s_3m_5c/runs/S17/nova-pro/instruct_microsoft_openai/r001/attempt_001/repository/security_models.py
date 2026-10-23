class EncryptRequest:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext

class EncryptResponse:
    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext

class DecryptRequest:
    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext

class DecryptResponse:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext