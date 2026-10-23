import base64
from typing import Optional


class EncryptRequest:
    def __init__(
        self,
        plaintext: str,
        key_name: str,
        additional_authenticated_data: Optional[str] = None,
    ):
        self.plaintext = plaintext
        self.key_name = key_name
        self.additional_authenticated_data = additional_authenticated_data


class EncryptResponse:
    def __init__(self, ciphertext: bytes, key_name: str):
        self.ciphertext = base64.b64encode(ciphertext).decode("utf-8")
        self.key_name = key_name


class DecryptRequest:
    def __init__(
        self,
        ciphertext: str,
        key_name: str,
        additional_authenticated_data: Optional[str] = None,
    ):
        self.ciphertext = ciphertext
        self.key_name = key_name
        self.additional_authenticated_data = additional_authenticated_data


class DecryptResponse:
    def __init__(self, plaintext: bytes, key_name: str):
        self.plaintext = plaintext.decode("utf-8")
        self.key_name = key_name


class EnvelopeEncryptRequest:
    def __init__(self, plaintext: str, kms_key_name: str):
        self.plaintext = plaintext
        self.kms_key_name = kms_key_name


class EnvelopeEncryptResponse:
    def __init__(self, encrypted_data_key: bytes, ciphertext: bytes):
        self.encrypted_data_key = base64.b64encode(encrypted_data_key).decode("utf-8")
        self.ciphertext = base64.b64encode(ciphertext).decode("utf-8")


class SignRequest:
    def __init__(self, data: str, key_name: str):
        self.data = data
        self.key_name = key_name


class SignResponse:
    def __init__(self, signature: bytes, key_name: str):
        self.signature = base64.b64encode(signature).decode("utf-8")
        self.key_name = key_name


class VerifyRequest:
    def __init__(self, data: str, signature: str, key_name: str):
        self.data = data
        self.signature = signature
        self.key_name = key_name


class VerifyResponse:
    def __init__(self, is_valid: bool, key_name: str):
        self.is_valid = is_valid
        self.key_name = key_name
