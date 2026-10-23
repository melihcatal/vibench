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
class EncryptionRequest:
    plaintext: str
    key_id: Optional[str] = None
    context: Optional[Dict[str, str]] = None


@dataclass
class EncryptionResponse:
    ciphertext: str
    key_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: Optional[str] = None


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: Optional[str] = None


@dataclass
class SignRequest:
    message: str
    key_id: Optional[str] = None
    algorithm: str = "RSA_PKCS1_SHA256"


@dataclass
class SignResponse:
    signature: str
    key_id: Optional[str] = None
