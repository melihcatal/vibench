class EncryptionResponse:
    def __init__(self, ciphertext, iv, tag, key_id, algorithm):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id
        self.algorithm = algorithm

class DecryptionResponse:
    def __init__(self, plaintext):
        self.plaintext = plaintext

class SignatureResponse:
    def __init__(self, signature):
        self.signature = signature

class VerificationResponse:
    def __init__(self, is_valid):
        self.is_valid = is_valid