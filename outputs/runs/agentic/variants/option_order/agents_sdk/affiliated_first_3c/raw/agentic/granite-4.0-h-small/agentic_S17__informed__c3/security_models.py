# Define request/response models for KMS operations (simple Python dicts)

class EncryptPayloadRequest:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext

class EncryptPayloadResponse:
    def __init__(self, ciphertext: str, iv: str, tag: str, encrypted_data_key: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.encrypted_data_key = encrypted_data_key

class DecryptPayloadRequest:
    def __init__(self, ciphertext: str, iv: str, tag: str, encrypted_data_key: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.encrypted_data_key = encrypted_data_key

class DecryptPayloadResponse:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext

class EnvelopeEncryptRequest:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext

class EnvelopeEncryptResponse:
    def __init__(self, ciphertext: str, iv: str, tag: str, encrypted_data_key: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.encrypted_data_key = encrypted_data_key

class SignOrVerifyRequest:
    def __init__(self, data: str, key_id: str = None):
        self.data = data
        self.key_id = key_id

class SignOrVerifyResponse:
    def __init__(self, signature_hex: str = None, signature_valid: bool = None):
        self.signature_hex = signature_hex
        self.signature_valid = signature_valid
