from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    key: str
    data: bytes | None = None
    file_path: str | None = None
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadObjectResult:
    bucket: str
    key: str
    etag: str | None
    version_id: str | None
    uri: str


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in_seconds: int = 3600
    response_content_type: str | None = None


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket: str
    key: str
    content_length: int | None
    content_type: str | None
    etag: str | None
    last_modified: str | None
    version_id: str | None
    metadata: dict[str, str]


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
    next_continuation_token: str | None


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    job_id: str | None
    text: str
    page_count: int
    provider: str = "amazon-textract"


@dataclass(slots=True)
class TranslationResult:
    source_language: str | None
    target_language: str
    translated_text: str
    provider: str = "deepl"


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider: str = "openai"


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    provider: str = "openai"
    dimensions: int | None = None


def normalize_timestamp(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def coerce_metadata(value: dict[str, Any] | None) -> dict[str, str]:
    if not value:
        return {}
    return {str(k): str(v) for k, v in value.items()}
