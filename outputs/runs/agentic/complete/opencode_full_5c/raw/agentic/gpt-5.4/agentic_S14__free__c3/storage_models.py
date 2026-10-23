from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class StorageLocation:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    key: str
    data: bytes | None = None
    file_path: str | None = None
    content_type: str | None = None
    metadata: dict[str, str] | None = None


@dataclass(slots=True)
class UploadObjectResponse:
    bucket: str
    key: str
    etag: str | None
    version_id: str | None
    provider: str = "aws_s3"


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    response_content_type: str | None = None


@dataclass(slots=True)
class PresignedDownloadResponse:
    url: str
    expires_in: int
    bucket: str
    key: str
    provider: str = "aws_s3"


@dataclass(slots=True)
class ObjectMetadataResponse:
    bucket: str
    key: str
    size: int | None
    etag: str | None
    content_type: str | None
    last_modified: str | None
    metadata: dict[str, str]
    version_id: str | None
    provider: str = "aws_s3"


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int
    etag: str | None
    last_modified: str | None


@dataclass(slots=True)
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[ListedObject]
    continuation_token: str | None
    provider: str = "aws_s3"


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    page_count: int
    provider: str = "google_document_ai"


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    provider: str = "google_cloud_translate"


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


def isoformat_or_none(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def normalize_s3_head(
    bucket: str, key: str, payload: dict[str, Any]
) -> ObjectMetadataResponse:
    return ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        size=payload.get("ContentLength"),
        etag=payload.get("ETag"),
        content_type=payload.get("ContentType"),
        last_modified=isoformat_or_none(payload.get("LastModified")),
        metadata=payload.get("Metadata") or {},
        version_id=payload.get("VersionId"),
    )


def normalize_s3_list(
    bucket: str, prefix: str, payload: dict[str, Any]
) -> ListPrefixResponse:
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size", 0),
            etag=item.get("ETag"),
            last_modified=isoformat_or_none(item.get("LastModified")),
        )
        for item in payload.get("Contents", [])
    ]
    return ListPrefixResponse(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        continuation_token=payload.get("NextContinuationToken"),
    )
