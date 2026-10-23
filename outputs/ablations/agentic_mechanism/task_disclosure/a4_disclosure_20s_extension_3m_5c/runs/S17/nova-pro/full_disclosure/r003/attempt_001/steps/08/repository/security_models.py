from typing import Dict, Any


class EncryptionRequest:
    def __init__(self, key_id: str, plaintext: bytes):
        self.key_id = key_id
        self.plaintext = plaintext


class EncryptionResponse:
    def __init__(self, ciphertext_blob: bytes):
        self.ciphertext_blob = ciphertext_blob


class DecryptionRequest:
    def __init__(self, ciphertext_blob: bytes):
        self.ciphertext_blob = ciphertext_blob


class DecryptionResponse:
    def __init__(self, plaintext: bytes):
        self.plaintext = plaintext


def normalize_encryption_response(response: Dict[str, Any]) -> EncryptionResponse:
    return EncryptionResponse(ciphertext_blob=response['CiphertextBlob'])


def normalize_decryption_response(response: Dict[str, Any]) -> DecryptionResponse:
    return DecryptionResponse(plaintext=response['Plaintext'])