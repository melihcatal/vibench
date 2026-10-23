from dataclasses import dataclass
from typing import Any


@dataclass
class PayloadRequest:
    plaintext: str


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value).strip()


def normalize_key_id(value: Any) -> str:
    return normalize_text(value)
