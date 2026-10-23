from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
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
    version_id: Optional[str] = None
    provider: str = "amazon_s3"


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int]
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    provider: str = "amazon_s3"


@dataclass(slots=True)
class ListedObject:
    key: str
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str] = None


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    next_continuation_token: Optional[str] = None
    provider: str = "amazon_s3"


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    page_count: int
    provider: str = "amazon_textract"


@dataclass(slots=True)
class TranslationResult:
    text: str
    source_language: Optional[str]
    target_language: str
    provider: str = "deepl"


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
    provider: str = "cohere"


def to_iso8601(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_s3_metadata(bucket: str, key: str, response: Dict[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=_strip_quotes(response.get("ETag")),
        last_modified=to_iso8601(response.get("LastModified")),
        metadata=response.get("Metadata") or {},
        storage_class=response.get("StorageClass"),
        version_id=response.get("VersionId"),
    )


def normalize_s3_list(bucket: str, prefix: str, contents: Iterable[Dict[str, Any]], next_token: Optional[str]) -> ListPrefixResult:
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size"),
            etag=_strip_quotes(item.get("ETag")),
            last_modified=to_iso8601(item.get("LastModified")),
            storage_class=item.get("StorageClass"),
        )
        for item in contents
    ]
    return ListPrefixResult(bucket=bucket, prefix=prefix, objects=objects, next_continuation_token=next_token)


def _strip_quotes(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return value.strip('"')
