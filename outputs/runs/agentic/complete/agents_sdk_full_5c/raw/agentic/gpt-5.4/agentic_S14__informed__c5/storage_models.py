from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class StorageObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class UploadRequest:
    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    size: Optional[int] = None


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: Optional[str] = None


@dataclass
class ListedObject:
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    next_token: Optional[str] = None
    is_truncated: bool = False


@dataclass
class OCRResult:
    provider: str
    bucket: str
    key: str
    text: str
    page_count: Optional[int] = None
    raw_blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str


@dataclass
class SummaryResult:
    provider: str
    model: str
    summary: str


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int


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
        etag=_strip_quotes(response.get("ETag")),
        version_id=response.get("VersionId"),
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=to_iso8601(response.get("LastModified")),
        metadata=response.get("Metadata", {}) or {},
        storage_class=response.get("StorageClass"),
    )


def normalize_s3_list_item(item: Dict[str, Any]) -> ListedObject:
    return ListedObject(
        key=item["Key"],
        size=item.get("Size"),
        etag=_strip_quotes(item.get("ETag")),
        last_modified=to_iso8601(item.get("LastModified")),
        storage_class=item.get("StorageClass"),
    )


def model_dump(instance: Any) -> Dict[str, Any]:
    return asdict(instance)


def _strip_quotes(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return value.strip('"')
