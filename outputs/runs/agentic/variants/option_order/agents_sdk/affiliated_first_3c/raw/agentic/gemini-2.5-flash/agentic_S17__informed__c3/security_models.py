class EncryptionRequest:
    def __init__(self, plaintext: str, key_name: str):
        self.plaintext = plaintext
        self.key_name = key_name

class EncryptionResponse:
    def __init__(self, ciphertext: bytes, key_name: str):
        self.ciphertext = ciphertext
        self.key_name = key_name

class DecryptionRequest:
    def __init__(self, ciphertext: bytes, key_name: str):
        self.ciphertext = ciphertext
        self.key_name = key_name

class DecryptionResponse:
    def __init__(self, plaintext: str, key_name: str):
        self.plaintext = plaintext
        self.key_name = key_name

class EnvelopeEncryptionRequest:
    def __init__(self, plaintext: str, key_name: str):
        self.plaintext = plaintext
        self.key_name = key_name

class EnvelopeEncryptionResponse:
    def __init__(self, ciphertext: bytes, encrypted_data_key: bytes, key_name: str):
        self.ciphertext = ciphertext
        self.encrypted_data_key = encrypted_data_key
        self.key_name = key_name

class SigningRequest:
    def __init__(self, message: bytes, key_name: str):
        self.message = message
        self.key_name = key_name

class SigningResponse:
    def __init__(self, signature: bytes, key_name: str):
        self.signature = signature
        self.key_name = key_name

class VerificationRequest:
    def __init__(self, message: bytes, signature: bytes, key_name: str):
        self.message = message
        self.signature = signature
        self.key_name = key_name

class VerificationResponse:
    def __init__(self, is_valid: bool, key_name: str):
        self.is_valid = is_valid
        self.key_name = key_name
