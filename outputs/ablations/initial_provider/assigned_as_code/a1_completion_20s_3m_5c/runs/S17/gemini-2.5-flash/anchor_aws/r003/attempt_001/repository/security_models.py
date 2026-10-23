class EncryptionRequest:
    def __init__(self, plaintext: bytes, key_id: str, region: str = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.region = region

class EncryptionResponse:
    def __init__(self, ciphertext: bytes):
        self.ciphertext = ciphertext

class DecryptionRequest:
    def __init__(self, ciphertext: bytes, key_id: str, region: str = None):
        self.ciphertext = ciphertext
        self.key_id = key_id
        self.region = region

class DecryptionResponse:
    def __init__(self, plaintext: bytes):
        self.plaintext = plaintext

class SignRequest:
    def __init__(self, message: bytes, key_id: str, signing_algorithm: str = None, region: str = None):
        self.message = message
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm
        self.region = region

class SignResponse:
    def __init__(self, signature: bytes):
        self.signature = signature

class VerifyRequest:
    def __init__(self, message: bytes, signature: bytes, key_id: str, signing_algorithm: str = None, region: str = None):
        self.message = message
        self.signature = signature
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm
        self.region = region

class VerifyResponse:
    def __init__(self, signature_valid: bool):
        self.signature_valid = signature_valid