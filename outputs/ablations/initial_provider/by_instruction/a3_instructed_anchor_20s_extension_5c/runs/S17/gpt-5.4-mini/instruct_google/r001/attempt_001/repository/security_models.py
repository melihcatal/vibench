from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value).strip()


def normalize_dict(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return data or {}


@dataclass
class PayloadRequest:
    plaintext: str
    key_name: str
    location: str = "global"


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_name: str
    provider: str


@dataclass
class EnvelopeMaterial:
    encrypted_key: str
    ciphertext: str
    key_name: str
    provider: str


@dataclass
class SignedPayload:
    payload: str
    signature: str
    key_name: str
    provider: str
