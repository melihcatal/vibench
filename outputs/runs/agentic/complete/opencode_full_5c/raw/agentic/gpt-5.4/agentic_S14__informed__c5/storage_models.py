from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, BinaryIO


def _isoformat(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    object_name: str
    data: bytes | BinaryIO | None = None
    file_path: str | None = None
    content_type: str | None = None
    metadata: dict[str, str] | None = None


@dataclass(slots=True)
class UploadObjectResult:
    bucket: str
    object_name: str
    etag: str | None
    version_id: str | None
    content_type: str | None
    size: int | None


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    object_name: str
    expires_in_seconds: int = 3600
    response_content_type: str | None = None


@dataclass(slots=True)
class PresignedDownloadResult:
    bucket: str
    object_name: str
    url: str
    expires_in_seconds: int


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket: str
    object_name: str
    etag: str | None
    size: int | None
    content_type: str | None
    last_modified: str | None
    metadata: dict[str, str]
    version_id: str | None


@dataclass(slots=True)
class ListedObject:
    object_name: str
    size: int | None
    etag: str | None
    last_modified: str | None
    storage_class: str | None


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: list[ListedObject]
    next_token: str | None


@dataclass(slots=True)
class OcrDocumentResult:
    bucket: str
    object_name: str
    text: str
    page_count: int | None
    provider: str
    model: str


@dataclass(slots=True)
class TranslationResult:
    source_language: str | None
    target_language: str
    translated_text: str
    provider: str


@dataclass(slots=True)
class SummaryResult:
    summary: str
    provider: str
    model: str


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    dimensions: int
    provider: str
    model: str


def normalize_metadata_result(
    bucket: str, object_name: str, payload: dict[str, Any]
) -> ObjectMetadataResult:
    return ObjectMetadataResult(
        bucket=bucket,
        object_name=object_name,
        etag=payload.get("ETag"),
        size=payload.get("ContentLength"),
        content_type=payload.get("ContentType"),
        last_modified=_isoformat(payload.get("LastModified")),
        metadata=dict(payload.get("Metadata") or {}),
        version_id=payload.get("VersionId"),
    )


def normalize_listed_object(item: dict[str, Any]) -> ListedObject:
    return ListedObject(
        object_name=item["Key"],
        size=item.get("Size"),
        etag=item.get("ETag"),
        last_modified=_isoformat(item.get("LastModified")),
        storage_class=item.get("StorageClass"),
    )
