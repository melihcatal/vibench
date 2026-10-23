from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    return normalize_text(value).encode("utf-8")


def normalize_ciphertext_blob(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    text = normalize_text(value)
    try:
        return base64.b64decode(text, validate=True)
    except Exception:
        return text.encode("utf-8")


@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptResponse:
    key_id: str
    ciphertext_blob_b64: str

    @classmethod
    def from_kms_response(cls, response: Dict[str, Any], key_id: str) -> "EncryptResponse":
        return cls(key_id=key_id, ciphertext_blob_b64=base64.b64encode(response["CiphertextBlob"]).decode("utf-8"))

    def to_dict(self) -> Dict[str, Any]:
        return {"key_id": self.key_id, "ciphertext_blob_b64": self.ciphertext_blob_b64}


@dataclass
class DecryptRequest:
    ciphertext_blob: bytes
    key_id: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    plaintext: str

    @classmethod
    def from_kms_response(cls, response: Dict[str, Any]) -> "DecryptResponse":
        plaintext = response["Plaintext"]
        if isinstance(plaintext, bytes):
            plaintext = plaintext.decode("utf-8")
        return cls(plaintext=str(plaintext))

    def to_dict(self) -> Dict[str, Any]:
        return {"plaintext": self.plaintext}


@dataclass
class EnvelopeEncryptionResult:
    key_id: str
    encrypted_data_key: str
    nonce: str
    ciphertext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "encrypted_data_key": self.encrypted_data_key,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
            "encryption_context": self.encryption_context,
        }


@dataclass
class SignVerifyRequest:
    message: str
    signature_b64: Optional[str]
    key_id: str
    signing_algorithm: str


@dataclass
class SignVerifyResponse:
    action: str
    key_id: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"action": self.action, "key_id": self.key_id, "signature_b64": self.signature_b64, "verified": self.verified}
