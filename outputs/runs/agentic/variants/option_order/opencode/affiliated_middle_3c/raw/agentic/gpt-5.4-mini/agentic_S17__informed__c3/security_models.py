import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str
    context: Optional[Dict[str, str]] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str
    metadata: Dict[str, Any]


@dataclass
class EnvelopeBundle:
    wrapped_key: str
    data_key: str
    iv: str
    ciphertext: str
    key_id: str


def normalize_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (context or {}).items()}


def encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def decode_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))
