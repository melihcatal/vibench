from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return str(value).encode("utf-8")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


@dataclass
class PayloadRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class CiphertextResponse:
    key_id: str
    ciphertext: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionResponse:
    key_id: str
    plaintext: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SignatureRequest:
    key_id: str
    message: str


@dataclass
class VerificationResult:
    key_id: str
    verified: bool
    metadata: Optional[Dict[str, Any]] = None
