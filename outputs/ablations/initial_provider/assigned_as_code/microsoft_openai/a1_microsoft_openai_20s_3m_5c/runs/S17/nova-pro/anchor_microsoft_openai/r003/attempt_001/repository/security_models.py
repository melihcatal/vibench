class EncryptionResponse:
    def __init__(self, ciphertext, iv, tag, key_id, algorithm):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id
        self.algorithm = algorithm


class DecryptionResponse:
    def __init__(self, plaintext, key_id, algorithm):
        self.plaintext = plaintext
        self.key_id = key_id
        self.algorithm = algorithm


class SignatureResponse:
    def __init__(self, signature, key_id, algorithm):
        self.signature = signature
        self.key_id = key_id
        self.algorithm = algorithm
