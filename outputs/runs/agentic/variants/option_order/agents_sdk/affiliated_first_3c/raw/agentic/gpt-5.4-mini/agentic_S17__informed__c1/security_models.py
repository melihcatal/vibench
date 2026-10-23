from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_bytes(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, memoryview):
        return data.tobytes()
    return str(data).encode("utf-8")


def normalize_text(data: Any) -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode("utf-8", errors="replace")
    if isinstance(data, bytearray):
        return bytes(data).decode("utf-8", errors="replace")
    return str(data)


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: Optional[str] = None
    context: Dict[str, str] = field(default_factory=dict)


@dataclass
class CiphertextResponse:
    ciphertext_b64: str
    key_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptionResult:
    encrypted_data_key_b64: str
    ciphertext_b64: str
    key_id: Optional[str] = None
    algorithm: str = "AES256-GCM"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignatureResult:
    signature_b64: str
    verified: Optional[bool] = None
    key_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageSummary:
    provider: str
    key_id: str
    total_events: int
    encrypt_events: int = 0
    decrypt_events: int = 0
    sign_events: int = 0
    verify_events: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
