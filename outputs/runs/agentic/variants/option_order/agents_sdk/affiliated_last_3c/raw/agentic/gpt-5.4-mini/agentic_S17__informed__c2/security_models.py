from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class KeyOperationRequest:
    key_name: str
    plaintext: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    aad: Optional[bytes] = None
    digest: Optional[bytes] = None
    message: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyOperationResponse:
    key_name: str
    ciphertext: Optional[bytes] = None
    plaintext: Optional[bytes] = None
    signature: Optional[bytes] = None
    verified: Optional[bool] = None
    wrapped_data_key: Optional[bytes] = None
    nonce: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_bytes(value: Any) -> Optional[bytes]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, memoryview):
        return value.tobytes()
    if isinstance(value, bytearray):
        return bytes(value)
    raise TypeError(f"Unsupported byte-like value: {type(value)!r}")


def to_text(value: Optional[bytes]) -> Optional[str]:
    if value is None:
        return None
    return value.decode("utf-8", errors="replace")
