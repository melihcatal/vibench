class EncryptionRequest:
    def __init__(self, key_id, plaintext):
        self.key_id = key_id
        self.plaintext = plaintext

class EncryptionResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext