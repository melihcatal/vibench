class EncryptionRequest:
    def __init__(self, plaintext, key_id):
        self.plaintext = plaintext
        self.key_id = key_id


class EncryptionResponse:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext
