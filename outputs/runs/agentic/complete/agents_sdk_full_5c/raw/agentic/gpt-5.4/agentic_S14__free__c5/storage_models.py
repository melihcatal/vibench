from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


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
    checksum_sha256: Optional[str] = None


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    content_length: Optional[int]
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    version_id: Optional[str]
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ListedObject:
    key: str
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str]


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    page_count: int
    provider_job_id: Optional[str] = None


@dataclass(slots=True)
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str
    provider_request_id: Optional[str] = None


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider: str = "openai"


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    model: str
    provider: str = "openai"


def isoformat_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def normalize_s3_metadata(bucket: str, key: str, head: Dict[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        content_length=head.get("ContentLength"),
        content_type=head.get("ContentType"),
        etag=head.get("ETag"),
        last_modified=isoformat_or_none(head.get("LastModified")),
        version_id=head.get("VersionId"),
        metadata=head.get("Metadata") or {},
    )


def normalize_s3_listing(items: Optional[Iterable[Dict[str, Any]]]) -> List[ListedObject]:
    results: List[ListedObject] = []
    for item in items or []:
        results.append(
            ListedObject(
                key=item["Key"],
                size=item.get("Size"),
                etag=item.get("ETag"),
                last_modified=isoformat_or_none(item.get("LastModified")),
                storage_class=item.get("StorageClass"),
            )
        )
    return results
