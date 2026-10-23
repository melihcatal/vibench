class EncryptionRequest:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class EncryptionResponse:
    def __init__(self, result):
        self.result = result

class DecryptionRequest:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

class DecryptionResponse:
    def __init__(self, result):
        self.result = result

class SignRequest:
    def __init__(self, data):
        self.data = data

class SignResponse:
    def __init__(self, result):
        self.result = result