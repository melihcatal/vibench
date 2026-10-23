from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(slots=True)
class StorageLocation:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    key: str
    body: bytes | None = None
    file_path: str | None = None
    content_type: str | None = None
    metadata: dict[str, str] | None = None


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
class PresignedDownloadResult:
    bucket: str
    key: str
    url: str
    expires_at: datetime


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket: str
    key: str
    size: int | None
    content_type: str | None
    etag: str | None
    last_modified: datetime | None
    metadata: dict[str, str]
    version_id: str | None


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int | None
    etag: str | None
    last_modified: datetime | None
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
    text: str
    page_count: int
    provider_job_id: str | None


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str | None
    target_language: str
    provider: str


@dataclass(slots=True)
class SummaryResult:
    source_text: str
    summary: str
    model: str
    provider: str


@dataclass(slots=True)
class EmbeddingResult:
    input_text: str
    embedding: list[float]
    model: str
    dimensions: int
    provider: str


def s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def utc_expiration(expires_in_seconds: int) -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0) + timedelta_seconds(
        expires_in_seconds
    )


def timedelta_seconds(seconds: int):
    from datetime import timedelta

    return timedelta(seconds=seconds)


def normalize_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return None


def normalize_metadata_map(value: Mapping[str, Any] | None) -> dict[str, str]:
    if not value:
        return {}
    return {str(k): str(v) for k, v in value.items()}
