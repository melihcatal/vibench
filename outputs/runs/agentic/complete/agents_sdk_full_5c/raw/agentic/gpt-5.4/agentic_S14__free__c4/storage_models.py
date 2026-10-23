from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "StorageObjectRef":
        return cls(bucket=str(data["bucket"]), key=str(data["key"]))


@dataclass(slots=True)
class UploadRequest:
    bucket: str
    key: str
    file_path: str | None = None
    data: bytes | None = None
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadResult:
    bucket: str
    key: str
    etag: str | None
    version_id: str | None


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: int | None
    etag: str | None
    content_type: str | None
    last_modified: str | None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int | None
    etag: str | None
    last_modified: str | None
    storage_class: str | None


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    page_count: int
    provider_job_id: str | None = None


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str | None
    target_language: str


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    dimensions: int


def to_iso8601(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_s3_metadata(bucket: str, key: str, response: Mapping[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        etag=response.get("ETag"),
        content_type=response.get("ContentType"),
        last_modified=to_iso8601(response.get("LastModified")),
        metadata=dict(response.get("Metadata") or {}),
    )


def normalize_s3_list_item(item: Mapping[str, Any]) -> ListedObject:
    return ListedObject(
        key=str(item.get("Key", "")),
        size=item.get("Size"),
        etag=item.get("ETag"),
        last_modified=to_iso8601(item.get("LastModified")),
        storage_class=item.get("StorageClass"),
    )
