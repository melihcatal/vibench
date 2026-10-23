class EncryptRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class EncryptResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext