from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_bytes_payload(payload: Any) -> bytes:
    if payload is None:
        return b""
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, bytearray):
        return bytes(payload)
    if isinstance(payload, str):
        return payload.encode("utf-8")
    if isinstance(payload, dict) and "data" in payload:
        return normalize_bytes_payload(payload["data"])
    return str(payload).encode("utf-8")


def normalize_text_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="replace")
    return str(payload)


@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class SignRequest:
    message: bytes
    key_id: str


@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str


@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext: bytes
    algorithm: str
    metadata: Dict[str, Any]


@dataclass
class DecryptionResponse:
    key_id: str
    plaintext: bytes
    algorithm: str
    metadata: Dict[str, Any]


@dataclass
class SignResponse:
    key_id: str
    signature: bytes
    algorithm: str
    metadata: Dict[str, Any]


@dataclass
class VerifyResponse:
    key_id: str
    verified: bool
    algorithm: str
    metadata: Dict[str, Any]
