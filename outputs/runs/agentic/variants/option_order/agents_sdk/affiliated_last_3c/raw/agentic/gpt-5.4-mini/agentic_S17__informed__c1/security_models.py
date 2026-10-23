from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass
class KeyRequest:
    key_id: str
    plaintext: bytes
    aad: bytes = b""
    algorithm: str = "AES_256_GCM"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CiphertextResponse:
    key_id: str
    ciphertext: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedResult:
    ok: bool
    provider: str
    key_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, memoryview):
        return value.tobytes()
    if isinstance(value, bytearray):
        return bytes(value)
    raise TypeError(f"Unsupported byte value type: {type(value)!r}")


def normalize_mapping(mapping: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not mapping:
        return {}
    return dict(mapping)
