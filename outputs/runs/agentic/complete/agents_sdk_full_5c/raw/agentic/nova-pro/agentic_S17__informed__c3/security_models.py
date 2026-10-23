class EncryptionRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class EncryptionResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext