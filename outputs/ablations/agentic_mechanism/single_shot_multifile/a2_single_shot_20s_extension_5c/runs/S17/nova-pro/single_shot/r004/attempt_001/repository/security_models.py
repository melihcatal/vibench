class EncryptionRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class EncryptionResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class DecryptionRequest:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class DecryptionResponse:
    def __init__(self, plaintext):
        self.plaintext = plaintext