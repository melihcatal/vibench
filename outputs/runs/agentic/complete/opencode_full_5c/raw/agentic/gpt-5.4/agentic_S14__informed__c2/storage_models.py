from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, BinaryIO


def _coerce_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(normalized)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def normalize_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(key): str(value) for key, value in metadata.items()}


@dataclass(slots=True)
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    data: bytes | BinaryIO
    content_type: str | None = None
    metadata: dict[str, str] | None = None


@dataclass(slots=True)
class UploadObjectResult:
    bucket_name: str
    object_name: str
    etag: str | None
    version_id: str | None
    size: int | None
    content_type: str | None
    metadata: dict[str, str]


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expires_in_seconds: int = 3600
    response_content_type: str | None = None


@dataclass(slots=True)
class PresignedDownloadResult:
    bucket_name: str
    object_name: str
    url: str
    expires_in_seconds: int


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket_name: str
    object_name: str
    size: int | None
    etag: str | None
    content_type: str | None
    last_modified: datetime | None
    metadata: dict[str, str]
    version_id: str | None

    @classmethod
    def from_s3_head(
        cls, bucket_name: str, object_name: str, head: dict[str, Any]
    ) -> "ObjectMetadataResult":
        return cls(
            bucket_name=bucket_name,
            object_name=object_name,
            size=head.get("ContentLength"),
            etag=(head.get("ETag") or "").strip('"') or None,
            content_type=head.get("ContentType"),
            last_modified=_coerce_datetime(head.get("LastModified")),
            metadata=normalize_metadata(head.get("Metadata")),
            version_id=head.get("VersionId"),
        )


@dataclass(slots=True)
class ListedObject:
    object_name: str
    size: int | None
    etag: str | None
    last_modified: datetime | None
    storage_class: str | None


@dataclass(slots=True)
class ListPrefixResult:
    bucket_name: str
    prefix: str
    objects: list[ListedObject]
    next_continuation_token: str | None


@dataclass(slots=True)
class OcrDocumentResult:
    bucket_name: str
    object_name: str
    pages: list[dict[str, Any]]
    full_text: str
    provider: str


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    provider: str


@dataclass(slots=True)
class AssetSummaryResult:
    summary: str
    model: str
    provider: str


@dataclass(slots=True)
class AssetEmbeddingResult:
    embedding: list[float]
    model: str
    provider: str
    dimensions: int
