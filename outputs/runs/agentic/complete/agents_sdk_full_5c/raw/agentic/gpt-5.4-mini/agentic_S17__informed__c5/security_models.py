from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass
class NormalizedKeyRequest:
    key_id: str
    plaintext: bytes = b""
    ciphertext: bytes = b""
    aad: bytes = b""
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedKeyResponse:
    key_id: str
    algorithm: str
    payload: bytes = b""
    nonce: bytes = b""
    tag: bytes = b""
    signature: bytes = b""
    metadata: Dict[str, Any] = field(default_factory=dict)


def coerce_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    return str(value).encode("utf-8")


def normalize_mapping(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in mapping.items():
        if isinstance(value, (bytes, bytearray)):
            normalized[key] = value.hex()
        else:
            normalized[key] = value
    return normalized
