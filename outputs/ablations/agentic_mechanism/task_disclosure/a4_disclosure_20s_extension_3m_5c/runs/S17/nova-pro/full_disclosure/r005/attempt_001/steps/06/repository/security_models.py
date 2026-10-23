from typing import Any, Dict


class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id


class EncryptionResponse:
    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext


class DecryptionRequest:
    def __init__(self, ciphertext: str, key_id: str):
        self.ciphertext = ciphertext
        self.key_id = key_id


class DecryptionResponse:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext


def normalize_request(request: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize request fields
    return request


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize response fields
    return response