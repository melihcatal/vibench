from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def _to_utc_iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, str):
        return value
    raise TypeError(f"Unsupported datetime value: {type(value)!r}")


def _normalize_metadata(metadata: Mapping[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(key): str(value) for key, value in metadata.items()}


def _normalize_tags(tags: Any) -> list[str]:
    if not tags:
        return []
    if isinstance(tags, str):
        return [tags]
    return [str(tag) for tag in tags]


def normalize_bucket_name(name: Any) -> str:
    if not isinstance(name, str):
        raise TypeError("Bucket name must be a string")
    normalized = name.strip().lower()
    if not normalized:
        raise ValueError("Bucket name cannot be empty")
    return normalized


def normalize_object_key(key: Any) -> str:
    if not isinstance(key, str):
        raise TypeError("Object key must be a string")
    normalized = key.strip().lstrip("/")
    if not normalized:
        raise ValueError("Object key cannot be empty")
    return normalized


@dataclass(slots=True)
class StorageRequest:
    bucket: str
    object_key: str | None = None
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    version_id: str | None = None

    def normalized(self) -> "StorageRequest":
        return StorageRequest(
            bucket=normalize_bucket_name(self.bucket),
            object_key=normalize_object_key(self.object_key) if self.object_key is not None else None,
            content_type=self.content_type.strip() if isinstance(self.content_type, str) and self.content_type.strip() else None,
            metadata=_normalize_metadata(self.metadata),
            tags=_normalize_tags(self.tags),
            version_id=self.version_id.strip() if isinstance(self.version_id, str) and self.version_id.strip() else None,
        )


@dataclass(slots=True)
class StorageResponse:
    bucket: str
    object_key: str | None = None
    etag: str | None = None
    size_bytes: int | None = None
    content_type: str | None = None
    last_modified: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    version_id: str | None = None
    storage_class: str | None = None

    @classmethod
    def from_provider(cls, payload: Mapping[str, Any]) -> "StorageResponse":
        return cls(
            bucket=normalize_bucket_name(payload.get("bucket", "")),
            object_key=normalize_object_key(payload["object_key"]) if payload.get("object_key") else None,
            etag=str(payload["etag"]) if payload.get("etag") is not None else None,
            size_bytes=int(payload["size_bytes"]) if payload.get("size_bytes") is not None else None,
            content_type=str(payload["content_type"]) if payload.get("content_type") is not None else None,
            last_modified=_to_utc_iso(payload.get("last_modified")),
            metadata=_normalize_metadata(payload.get("metadata")),
            tags=_normalize_tags(payload.get("tags")),
            version_id=str(payload["version_id"]) if payload.get("version_id") is not None else None,
            storage_class=str(payload["storage_class"]) if payload.get("storage_class") is not None else None,
        )


@dataclass(slots=True)
class ManagedObject:
    bucket: str
    key: str
    size_bytes: int | None = None
    etag: str | None = None
    content_type: str | None = None
    last_modified: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    version_id: str | None = None

    @classmethod
    def from_response(cls, response: StorageResponse) -> "ManagedObject":
        if response.object_key is None:
            raise ValueError("Response missing object key")
        return cls(
            bucket=response.bucket,
            key=response.object_key,
            size_bytes=response.size_bytes,
            etag=response.etag,
            content_type=response.content_type,
            last_modified=response.last_modified,
            metadata=dict(response.metadata),
            tags=list(response.tags),
            version_id=response.version_id,
        )


def normalize_storage_request(request: Mapping[str, Any] | StorageRequest) -> StorageRequest:
    if isinstance(request, StorageRequest):
        return request.normalized()
    return StorageRequest(
        bucket=normalize_bucket_name(request.get("bucket", "")),
        object_key=normalize_object_key(request["object_key"]) if request.get("object_key") is not None else None,
        content_type=request.get("content_type"),
        metadata=_normalize_metadata(request.get("metadata")),
        tags=_normalize_tags(request.get("tags")),
        version_id=request.get("version_id"),
    ).normalized()


def normalize_storage_response(payload: Mapping[str, Any] | StorageResponse) -> StorageResponse:
    if isinstance(payload, StorageResponse):
        return payload
    return StorageResponse.from_provider(payload)
