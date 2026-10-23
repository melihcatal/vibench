from typing import Dict, Any


class EncryptionRequest:
    def __init__(self, plaintext: bytes, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id


class EncryptionResponse:
    def __init__(self, ciphertext_blob: bytes):
        self.ciphertext_blob = ciphertext_blob


class DecryptionRequest:
    def __init__(self, ciphertext_blob: bytes):
        self.ciphertext_blob = ciphertext_blob


class DecryptionResponse:
    def __init__(self, plaintext: bytes):
        self.plaintext = plaintext


def normalize_request(request: Dict[str, Any]) -> Dict[str, Any]:
    normalized_request = {}
    for key, value in request.items():
        if isinstance(value, bytes):
            normalized_request[key] = value.decode('utf-8')
        else:
            normalized_request[key] = value
    return normalized_request


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {}
    for key, value in response.items():
        if isinstance(value, bytes):
            normalized_response[key] = value.decode('utf-8')
        else:
            normalized_response[key] = value
    return normalized_response
