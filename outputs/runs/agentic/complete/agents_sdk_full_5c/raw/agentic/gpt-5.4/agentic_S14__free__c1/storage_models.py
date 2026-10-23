from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class ObjectLocator:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadRequest:
    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    checksum_sha256: Optional[str]
    uri: str


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in_seconds: int = 3600
    response_content_type: Optional[str] = None


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    content_length: Optional[int]
    content_type: Optional[str]
    etag: Optional[str]
    version_id: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: Optional[str] = None


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int
    etag: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str]


@dataclass(slots=True)
class OCRResult:
    provider: str
    bucket: str
    key: str
    pages: int
    text: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str


@dataclass(slots=True)
class SummaryResult:
    provider: str
    model: str
    summary: str


@dataclass(slots=True)
class EmbeddingResult:
    provider: str
    model: str
    dimensions: int
    vector: List[float]


def isoformat_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    return str(value)


def s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def normalize_s3_head(bucket: str, key: str, head: Dict[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        content_length=head.get("ContentLength"),
        content_type=head.get("ContentType"),
        etag=head.get("ETag"),
        version_id=head.get("VersionId"),
        last_modified=isoformat_or_none(head.get("LastModified")),
        metadata=head.get("Metadata", {}) or {},
        storage_class=head.get("StorageClass"),
    )


def normalize_s3_list(contents: Optional[Iterable[Dict[str, Any]]]) -> List[ListedObject]:
    items: List[ListedObject] = []
    for entry in contents or []:
        items.append(
            ListedObject(
                key=entry["Key"],
                size=int(entry.get("Size", 0)),
                etag=entry.get("ETag"),
                last_modified=isoformat_or_none(entry.get("LastModified")),
                storage_class=entry.get("StorageClass"),
            )
        )
    return items
