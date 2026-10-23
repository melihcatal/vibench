from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_key_name(value: Any) -> str:
    text = normalize_text(value).strip()
    if not text:
        raise ValueError("key name is required")
    return text


def build_metadata(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


@dataclass
class PlaintextPayload:
    plaintext: str
    key_name: str
    metadata: Dict[str, Any]


@dataclass
class CiphertextPayload:
    ciphertext: str
    key_name: str
    metadata: Dict[str, Any]


@dataclass
class EnvelopePayload:
    encrypted_key: str
    ciphertext: str
    key_name: str
    metadata: Dict[str, Any]


@dataclass
class CryptoResult:
    ok: bool
    provider: str
    key_name: str
    payload: Dict[str, Any]
    error: Optional[str] = None
