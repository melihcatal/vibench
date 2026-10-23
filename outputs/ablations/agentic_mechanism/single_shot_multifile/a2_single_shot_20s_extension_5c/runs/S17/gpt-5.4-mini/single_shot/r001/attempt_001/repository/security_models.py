from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Dict


def _to_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        try:
            return base64.b64decode(value, validate=True)
        except Exception:
            return value.encode("utf-8")
    if isinstance(value, dict):
        if "data" in value:
            return _to_bytes(value["data"])
        if "plaintext" in value:
            return _to_bytes(value["plaintext"])
    raise TypeError("Unsupported payload type")


def normalize_plaintext_payload(payload: Any) -> bytes:
    return _to_bytes(payload)


def normalize_ciphertext_payload(payload: Any) -> bytes:
    return _to_bytes(payload)


def normalize_signature_payload(payload: Any) -> bytes:
    if isinstance(payload, dict) and "message" in payload:
        return _to_bytes(payload["message"])
    return _to_bytes(payload)


@dataclass
class BaseResult:
    key_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"key_name": self.key_name, "metadata": self.metadata}


@dataclass
class EncryptionResult(BaseResult):
    ciphertext: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["ciphertext"] = self.ciphertext
        return data


@dataclass
class DecryptionResult(BaseResult):
    plaintext: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["plaintext"] = self.plaintext
        return data


@dataclass
class EnvelopeEncryptionResult(BaseResult):
    encrypted_key: str = ""
    nonce: str = ""
    ciphertext: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({"encrypted_key": self.encrypted_key, "nonce": self.nonce, "ciphertext": self.ciphertext})
        return data


@dataclass
class SignatureResult(BaseResult):
    signature: str = ""
    verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        if self.signature:
            data["signature"] = self.signature
        data["verified"] = self.verified
        return data
