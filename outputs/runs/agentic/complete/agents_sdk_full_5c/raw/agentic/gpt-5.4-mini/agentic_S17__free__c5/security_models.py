from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    aad: Optional[str] = None


@dataclass
class PayloadResponse:
    key_id: str
    algorithm: str
    payload: Dict[str, Any]


@dataclass
class NormalizedPayload:
    raw: bytes
    text: Optional[str]


def normalize_text(value: str) -> NormalizedPayload:
    raw = value.encode("utf-8")
    return NormalizedPayload(raw=raw, text=value)


def normalize_b64(value: str) -> NormalizedPayload:
    raw = base64.b64decode(value.encode("utf-8"))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = None
    return NormalizedPayload(raw=raw, text=text)


def encode_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def response_payload(key_id: str, algorithm: str, **payload: Any) -> PayloadResponse:
    return PayloadResponse(key_id=key_id, algorithm=algorithm, payload=payload)
