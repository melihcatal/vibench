from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def isoformat_or_none(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(key): str(value) for key, value in metadata.items()}


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    key: str
    file_path: str | None = None
    data: bytes | None = None
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadObjectResult:
    bucket: str
    key: str
    etag: str | None
    version_id: str | None
    size: int | None = None


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    response_content_type: str | None = None


@dataclass(slots=True)
class PresignedDownloadResult:
    bucket: str
    key: str
    url: str
    expires_in: int


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket: str
    key: str
    etag: str | None
    content_length: int | None
    content_type: str | None
    last_modified: str | None
    version_id: str | None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ListedObject:
    key: str
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
    is_truncated: bool


@dataclass(slots=True)
class OCRDocumentResult:
    bucket: str
    key: str
    provider: str
    text: str
    page_count: int
    lines: list[str]


@dataclass(slots=True)
class TranslationResult:
    provider: str
    source_language: str | None
    target_language: str
    translated_text: str


@dataclass(slots=True)
class AssetSummaryResult:
    provider: str
    model: str
    summary: str


@dataclass(slots=True)
class AssetEmbeddingResult:
    provider: str
    model: str
    input_text: str
    embedding: list[float]
