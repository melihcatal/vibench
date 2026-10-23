from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def _isoformat_utc(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_dict(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {}
    return {str(key): value for key, value in payload.items() if value is not None}


@dataclass(slots=True)
class StorageRequest:
    bucket: str
    object_key: str
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    expires_at: datetime | str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "bucket": self.bucket,
            "object_key": self.object_key,
            "content_type": self.content_type,
            "metadata": _normalize_dict(self.metadata),
            "expires_at": _isoformat_utc(self.expires_at),
        }
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(slots=True)
class StorageResponse:
    bucket: str
    object_key: str
    url: str | None = None
    etag: str | None = None
    size: int | None = None
    content_type: str | None = None
    created_at: datetime | str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "StorageResponse":
        return cls(
            bucket=str(payload.get("bucket", "")),
            object_key=str(payload.get("object_key", "")),
            url=payload.get("url"),
            etag=payload.get("etag"),
            size=payload.get("size"),
            content_type=payload.get("content_type"),
            created_at=payload.get("created_at"),
            metadata=_normalize_dict(payload.get("metadata")),
        )

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "bucket": self.bucket,
            "object_key": self.object_key,
            "url": self.url,
            "etag": self.etag,
            "size": self.size,
            "content_type": self.content_type,
            "created_at": _isoformat_utc(self.created_at),
            "metadata": _normalize_dict(self.metadata),
        }
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(slots=True)
class NormalizedStorageObject:
    bucket: str
    key: str
    uri: str
    content_type: str | None = None
    size: int | None = None
    etag: str | None = None
    created_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_storage_object(payload: Mapping[str, Any]) -> NormalizedStorageObject:
    bucket = str(payload.get("bucket") or payload.get("bucket_name") or "")
    key = str(payload.get("object_key") or payload.get("key") or payload.get("name") or "")
    uri = str(payload.get("uri") or payload.get("url") or f"storage://{bucket}/{key}")
    created_at = _isoformat_utc(payload.get("created_at") or payload.get("createdAt"))
    return NormalizedStorageObject(
        bucket=bucket,
        key=key,
        uri=uri,
        content_type=payload.get("content_type") or payload.get("mime_type"),
        size=payload.get("size"),
        etag=payload.get("etag"),
        created_at=created_at,
        metadata=_normalize_dict(payload.get("metadata")),
    )
