from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


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
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    checksum_sha256: Optional[str] = None


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    version_id: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    storage_class: Optional[str] = None


@dataclass(slots=True)
class ListedObject:
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    page_count: int = 0
    provider: str = "amazon-textract"


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
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
    dimensions: int
    provider: str = "cohere"


def to_dict(model: Any) -> dict[str, Any]:
    if hasattr(model, "__dataclass_fields__"):
        return asdict(model)
    raise TypeError("Expected dataclass instance")


def isoformat_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    return str(value)


def normalize_s3_head(bucket: str, key: str, response: Mapping[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        etag=_strip_quotes(response.get("ETag")),
        content_type=response.get("ContentType"),
        last_modified=isoformat_or_none(response.get("LastModified")),
        version_id=response.get("VersionId"),
        metadata=dict(response.get("Metadata") or {}),
        storage_class=response.get("StorageClass"),
    )


def normalize_s3_list_item(item: Mapping[str, Any]) -> ListedObject:
    return ListedObject(
        key=str(item.get("Key", "")),
        size=item.get("Size"),
        etag=_strip_quotes(item.get("ETag")),
        last_modified=isoformat_or_none(item.get("LastModified")),
        storage_class=item.get("StorageClass"),
    )


def _strip_quotes(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value).strip('"')
