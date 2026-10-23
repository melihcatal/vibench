class EncryptRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class DecryptRequest:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class SignRequest:
    def __init__(self, message):
        self.message = message