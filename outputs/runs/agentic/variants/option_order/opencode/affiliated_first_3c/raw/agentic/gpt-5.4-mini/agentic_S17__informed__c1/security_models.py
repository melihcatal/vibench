import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: Optional[str] = None


@dataclass
class CiphertextResponse:
    ciphertext_blob: str
    key_id: Optional[str] = None


@dataclass
class PlaintextResponse:
    plaintext: str
    key_id: Optional[str] = None


@dataclass
class NormalizedEvent:
    action: str
    key_id: Optional[str]
    metadata: Dict[str, Any]


def encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')


def decode_bytes(text: str) -> bytes:
    return base64.b64decode(text.encode('utf-8'))


def normalize_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value)
