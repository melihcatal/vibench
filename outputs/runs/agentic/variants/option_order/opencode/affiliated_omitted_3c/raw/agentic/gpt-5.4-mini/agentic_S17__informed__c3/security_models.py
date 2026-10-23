from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value).strip()


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    return normalize_text(value).encode("utf-8")


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str
    context: Optional[Dict[str, str]] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str
    provider: str


@dataclass
class EncryptionEnvelope:
    encrypted_data_key: str
    ciphertext: str
    key_id: str
    provider: str


@dataclass
class CryptoResult:
    success: bool
    payload: str
    key_id: str
    provider: str
