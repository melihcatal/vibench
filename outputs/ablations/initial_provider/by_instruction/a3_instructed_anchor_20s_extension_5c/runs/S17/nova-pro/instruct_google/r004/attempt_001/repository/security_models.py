class EncryptRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class DecryptRequest:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class EncryptResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class DecryptResponse:
    def __init__(self, plaintext):
        self.plaintext = plaintext
