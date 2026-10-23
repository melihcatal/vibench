class EncryptionRequest:
    def __init__(self, key_name, plaintext):
        self.key_name = key_name
        self.plaintext = plaintext

class EncryptionResponse:
    def __init__(self, result):
        self.result = result