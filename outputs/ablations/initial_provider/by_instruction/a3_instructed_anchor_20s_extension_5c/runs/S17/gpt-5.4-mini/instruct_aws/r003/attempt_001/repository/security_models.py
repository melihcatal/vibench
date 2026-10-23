import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def _b64decode_text(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_plaintext(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return str(value).encode("utf-8")


def normalize_key_id(value: Any) -> str:
    if value is None:
        raise ValueError("key_id is required")
    return str(value).strip()


@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "EncryptRequest":
        return cls(plaintext=normalize_plaintext(payload.get("plaintext")), key_id=normalize_key_id(payload.get("key_id")))


@dataclass
class EncryptResponse:
    ciphertext_blob: str
    key_id: str

    def to_payload(self) -> Dict[str, str]:
        return {"ciphertext_blob": self.ciphertext_blob, "key_id": self.key_id}


@dataclass
class DecryptRequest:
    ciphertext_blob: bytes
    key_id: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "DecryptRequest":
        return cls(ciphertext_blob=_b64decode_text(str(payload.get("ciphertext_blob", ""))), key_id=payload.get("key_id"))


@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str

    def to_payload(self) -> Dict[str, str]:
        return {"plaintext": self.plaintext, "key_id": self.key_id}


@dataclass
class EnvelopeCiphertext:
    encrypted_data_key: str
    iv: str
    ciphertext: str
    key_id: str

    def to_payload(self) -> Dict[str, str]:
        return {"encrypted_data_key": self.encrypted_data_key, "iv": self.iv, "ciphertext": self.ciphertext, "key_id": self.key_id}


@dataclass
class SignRequest:
    message: bytes
    key_id: str

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "SignRequest":
        return cls(message=normalize_plaintext(payload.get("message")), key_id=normalize_key_id(payload.get("key_id")))


@dataclass
class SignResponse:
    signature: str
    verified: Optional[bool]
    key_id: str

    def to_payload(self) -> Dict[str, Any]:
        return {"signature": self.signature, "verified": self.verified, "key_id": self.key_id}
