import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


def b64encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode_str(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str


@dataclass
class SignatureRequest:
    message: str
    key_id: str


@dataclass
class VerificationResult:
    valid: bool
    key_id: str


def response_dict(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}
