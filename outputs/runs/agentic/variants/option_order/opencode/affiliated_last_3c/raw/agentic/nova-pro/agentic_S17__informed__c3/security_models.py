class EncryptionResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext


class DecryptionResponse:
    def __init__(self, plaintext):
        self.plaintext = plaintext


class SignatureResponse:
    def __init__(self, signature):
        self.signature = signature
