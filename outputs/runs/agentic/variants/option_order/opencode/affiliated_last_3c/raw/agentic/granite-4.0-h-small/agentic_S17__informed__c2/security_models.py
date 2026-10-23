from typing import Any, Dict, List


class EncryptionRequest:
    def __init__(self, plaintext: str, key_name: str):
        self.plaintext = plaintext
        self.key_name = key_name

    def to_dict(self) -> Dict[str, Any]:
        return {"plaintext": self.plaintext, "key_name": self.key_name}


class DecryptionRequest:
    def __init__(self, ciphertext_blob: bytes, key_name: str):
        self.ciphertext_blob = ciphertext_blob
        self.key_name = key_name


class EncryptionResponse:
    def __init__(self, ciphertext: str, context: Dict[str, Any]):
        self.ciphertext = ciphertext
        self.context = context

    def to_dict(self) -> Dict[str, Any]:
        return {"ciphertext": self.ciphertext, "context": self.context}


class DecryptionResponse:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext


class SigningRequest:
    def __init__(self, key_name: str, message: bytes):
        self.key_name = key_name
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {"key_name": self.key_name, "message": self.message.decode("utf-8")}


class SignatureResponse:
    def __init__(self, signature: bytes):
        self.signature = signature

    def to_dict(self) -> Dict[str, Any]:
        return {"signature": self.signature.hex()}
