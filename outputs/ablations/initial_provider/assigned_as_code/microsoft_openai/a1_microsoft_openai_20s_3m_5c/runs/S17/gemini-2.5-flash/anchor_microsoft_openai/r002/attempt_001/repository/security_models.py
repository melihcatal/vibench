import base64
from typing import Dict, Any

class EncryptionRequest:
    def __init__(self, plaintext: bytes, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id

class EncryptionResponse:
    def __init__(self, ciphertext: bytes, iv: bytes, tag: bytes, key_id: str, algorithm: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id
        self.algorithm = algorithm

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext": base64.b64encode(self.ciphertext).decode('utf-8'),
            "iv": base64.b64encode(self.iv).decode('utf-8'),
            "tag": base64.b64encode(self.tag).decode('utf-8'),
            "key_id": self.key_id,
            "algorithm": self.algorithm
        }

class DecryptionRequest:
    def __init__(self, ciphertext: bytes, iv: bytes, tag: bytes, key_id: str, algorithm: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id
        self.algorithm = algorithm

class DecryptionResponse:
    def __init__(self, plaintext: bytes, key_id: str, algorithm: str):
        self.plaintext = plaintext
        self.key_id = key_id
        self.algorithm = algorithm

class EnvelopeEncryptionRequest:
    def __init__(self, plaintext: bytes, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id

class EnvelopeEncryptionResponse:
    def __init__(self, encrypted_data_key: bytes, ciphertext: bytes, iv: bytes, tag: bytes, key_id: str, algorithm: str):
        self.encrypted_data_key = encrypted_data_key
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id
        self.algorithm = algorithm

class SignRequest:
    def __init__(self, digest: bytes, key_id: str):
        self.digest = digest
        self.key_id = key_id

class SignResponse:
    def __init__(self, signature: bytes, key_id: str, algorithm: str):
        self.signature = signature
        self.key_id = key_id
        self.algorithm = algorithm

class VerifyRequest:
    def __init__(self, digest: bytes, signature: bytes, key_id: str, algorithm: str):
        self.digest = digest
        self.signature = signature
        self.key_id = key_id
        self.algorithm = algorithm

class VerifyResponse:
    def __init__(self, is_valid: bool):
        self.is_valid = is_valid
