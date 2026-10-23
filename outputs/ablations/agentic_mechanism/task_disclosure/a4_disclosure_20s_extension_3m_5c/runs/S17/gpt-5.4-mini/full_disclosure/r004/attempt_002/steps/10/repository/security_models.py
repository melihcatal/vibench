from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
import base64


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text or None
    return str(value).strip() or None


def _normalize_bytes(value: Any) -> Optional[bytes]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, memoryview):
        return value.tobytes()
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return None
        try:
            return base64.b64decode(raw, validate=True)
        except Exception:
            return raw.encode("utf-8")
    raise TypeError(f"Unsupported bytes value: {type(value)!r}")


def _normalize_metadata(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise TypeError("metadata must be a mapping")
    result: dict[str, str] = {}
    for key, item in value.items():
        k = _normalize_string(key)
        v = _normalize_string(item)
        if k is not None and v is not None:
            result[k] = v
    return result


@dataclass(slots=True)
class KeyMaterialRequest:
    key_id: str
    plaintext: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    associated_data: Optional[bytes] = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.key_id = _normalize_string(self.key_id) or ""
        self.plaintext = _normalize_bytes(self.plaintext)
        self.ciphertext = _normalize_bytes(self.ciphertext)
        self.associated_data = _normalize_bytes(self.associated_data)
        self.metadata = _normalize_metadata(self.metadata)


@dataclass(slots=True)
class KeyMaterialResponse:
    key_id: str
    success: bool
    plaintext: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    algorithm: Optional[str] = None
    version: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        self.key_id = _normalize_string(self.key_id) or ""
        self.algorithm = _normalize_string(self.algorithm)
        self.version = _normalize_string(self.version)
        self.plaintext = _normalize_bytes(self.plaintext)
        self.ciphertext = _normalize_bytes(self.ciphertext)
        self.metadata = _normalize_metadata(self.metadata)
        if self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
        else:
            self.created_at = self.created_at.astimezone(timezone.utc)


def normalize_key_id(value: Any) -> str:
    normalized = _normalize_string(value)
    if not normalized:
        raise ValueError("key_id is required")
    return normalized


def normalize_plaintext(value: Any) -> bytes:
    normalized = _normalize_bytes(value)
    if normalized is None:
        raise ValueError("plaintext is required")
    return normalized


def normalize_ciphertext(value: Any) -> bytes:
    normalized = _normalize_bytes(value)
    if normalized is None:
        raise ValueError("ciphertext is required")
    return normalized


def normalize_associated_data(value: Any) -> bytes:
    normalized = _normalize_bytes(value)
    if normalized is None:
        return b""
    return normalized


def normalize_metadata(value: Any) -> dict[str, str]:
    return _normalize_metadata(value)


def request_to_dict(request: KeyMaterialRequest) -> dict[str, Any]:
    return {
        "key_id": request.key_id,
        "plaintext": request.plaintext,
        "ciphertext": request.ciphertext,
        "associated_data": request.associated_data,
        "metadata": dict(request.metadata),
    }


def response_to_dict(response: KeyMaterialResponse) -> dict[str, Any]:
    payload = asdict(response)
    payload["created_at"] = response.created_at.isoformat()
    return payload
