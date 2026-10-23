import base64
from typing import Optional, Dict, Any


class EncryptionRequest:
    def __init__(
        self,
        plaintext: str,
        key_id: str,
        encryption_context: Optional[Dict[str, str]] = None,
    ):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = (
            encryption_context if encryption_context is not None else {}
        )


class EncryptionResponse:
    def __init__(
        self,
        ciphertext_blob: bytes,
        key_id: str,
        encryption_context: Optional[Dict[str, str]] = None,
    ):
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id
        self.encryption_context = (
            encryption_context if encryption_context is not None else {}
        )

    def to_dict(self):
        return {
            "ciphertext_blob": base64.b64encode(self.ciphertext_blob).decode("utf-8"),
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            ciphertext_blob=base64.b64decode(data["ciphertext_blob"]),
            key_id=data["key_id"],
            encryption_context=data.get("encryption_context", {}),
        )


class DecryptionRequest:
    def __init__(
        self,
        ciphertext_blob: bytes,
        encryption_context: Optional[Dict[str, str]] = None,
    ):
        self.ciphertext_blob = ciphertext_blob
        self.encryption_context = (
            encryption_context if encryption_context is not None else {}
        )


class DecryptionResponse:
    def __init__(
        self,
        plaintext: str,
        key_id: str,
        encryption_context: Optional[Dict[str, str]] = None,
    ):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = (
            encryption_context if encryption_context is not None else {}
        )

    def to_dict(self):
        return {
            "plaintext": self.plaintext,
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
        }


class EnvelopeEncryptionRequest:
    def __init__(
        self,
        plaintext: str,
        key_id: str,
        encryption_context: Optional[Dict[str, str]] = None,
    ):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = (
            encryption_context if encryption_context is not None else {}
        )


class EnvelopeEncryptionResponse:
    def __init__(
        self,
        encrypted_data_key: bytes,
        ciphertext_payload: bytes,
        key_id: str,
        encryption_context: Optional[Dict[str, str]] = None,
    ):
        self.encrypted_data_key = encrypted_data_key
        self.ciphertext_payload = ciphertext_payload
        self.key_id = key_id
        self.encryption_context = (
            encryption_context if encryption_context is not None else {}
        )

    def to_dict(self):
        return {
            "encrypted_data_key": base64.b64encode(self.encrypted_data_key).decode(
                "utf-8"
            ),
            "ciphertext_payload": base64.b64encode(self.ciphertext_payload).decode(
                "utf-8"
            ),
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            encrypted_data_key=base64.b64decode(data["encrypted_data_key"]),
            ciphertext_payload=base64.b64decode(data["ciphertext_payload"]),
            key_id=data["key_id"],
            encryption_context=data.get("encryption_context", {}),
        )


class SignatureRequest:
    def __init__(self, message: bytes, key_id: str, signing_algorithm: str):
        self.message = message
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm


class SignatureResponse:
    def __init__(self, signature: bytes, key_id: str, signing_algorithm: str):
        self.signature = signature
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm

    def to_dict(self):
        return {
            "signature": base64.b64encode(self.signature).decode("utf-8"),
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
        }


class VerificationRequest:
    def __init__(
        self, message: bytes, signature: bytes, key_id: str, signing_algorithm: str
    ):
        self.message = message
        self.signature = signature
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm


class VerificationResponse:
    def __init__(self, is_valid: bool, key_id: str, signing_algorithm: str):
        self.is_valid = is_valid
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm

    def to_dict(self):
        return {
            "is_valid": self.is_valid,
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
        }
