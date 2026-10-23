import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    payload: str
    key_id: Optional[str] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str


@dataclass
class PlaintextResponse:
    plaintext: str
    key_id: str


def ensure_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8")
    return str(value)


def to_b64(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def from_b64(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_mapping(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in data.items():
        normalized[key] = ensure_text(value)
    return normalized
