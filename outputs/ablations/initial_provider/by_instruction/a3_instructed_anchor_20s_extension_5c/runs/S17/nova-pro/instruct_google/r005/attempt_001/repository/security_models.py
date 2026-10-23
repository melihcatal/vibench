class EncryptionRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class DecryptionRequest:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class SignatureRequest:
    def __init__(self, data):
        self.data = data