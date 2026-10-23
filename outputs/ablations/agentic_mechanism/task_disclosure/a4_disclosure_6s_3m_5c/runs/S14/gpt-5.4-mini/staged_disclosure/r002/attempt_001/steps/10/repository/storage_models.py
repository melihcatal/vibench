from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def _to_utc_iso(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, str):
        return value
    return str(value)


def _normalize_dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _normalize_list(value: Any) -> List[Any]:
    return list(value) if isinstance(value, Iterable) and not isinstance(value, (str, bytes, Mapping)) else []


@dataclass(frozen=True)
class ManagedObjectStorageRequest:
    bucket: str
    key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    content_type: Optional[str] = None
    expires_at: Optional[Any] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"bucket": self.bucket}
        if self.key is not None:
            payload["key"] = self.key
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        if self.content_type is not None:
            payload["content_type"] = self.content_type
        if self.expires_at is not None:
            payload["expires_at"] = _to_utc_iso(self.expires_at)
        return payload


@dataclass(frozen=True)
class ManagedObjectStorageResponse:
    bucket: str
    key: Optional[str] = None
    etag: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedObjectStorageResponse":
        data = _normalize_dict(payload)
        return cls(
            bucket=str(data.get("bucket", "")),
            key=data.get("key"),
            etag=data.get("etag"),
            size=data.get("size"),
            content_type=data.get("content_type"),
            metadata=_normalize_dict(data.get("metadata")),
            created_at=_to_utc_iso(data.get("created_at")),
            updated_at=_to_utc_iso(data.get("updated_at")),
            raw=data,
        )


@dataclass(frozen=True)
class ManagedObjectStorageListResponse:
    items: List[ManagedObjectStorageResponse] = field(default_factory=list)
    next_cursor: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedObjectStorageListResponse":
        data = _normalize_dict(payload)
        items = [ManagedObjectStorageResponse.from_payload(item) for item in _normalize_list(data.get("items")) if isinstance(item, Mapping)]
        return cls(items=items, next_cursor=data.get("next_cursor"), raw=data)


def normalize_storage_request(payload: Mapping[str, Any]) -> ManagedObjectStorageRequest:
    data = _normalize_dict(payload)
    return ManagedObjectStorageRequest(
        bucket=str(data.get("bucket", "")),
        key=data.get("key"),
        metadata=_normalize_dict(data.get("metadata")),
        content_type=data.get("content_type"),
        expires_at=data.get("expires_at"),
    )


def normalize_storage_response(payload: Mapping[str, Any]) -> ManagedObjectStorageResponse:
    return ManagedObjectStorageResponse.from_payload(payload)


def normalize_storage_list(payload: Mapping[str, Any]) -> ManagedObjectStorageListResponse:
    return ManagedObjectStorageListResponse.from_payload(payload)
