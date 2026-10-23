from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class ManagedKeyRequest:
    key_id: str
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    aad: Optional[str] = None
    algorithm: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ManagedKeyResponse:
    key_id: str
    provider: str
    result: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CryptoEvent:
    event_type: str
    key_id: str
    provider: str
    status: str
    details: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value).strip()


def normalize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in data.items():
        if isinstance(value, str):
            normalized[key] = value.strip()
        else:
            normalized[key] = value
    return normalized
