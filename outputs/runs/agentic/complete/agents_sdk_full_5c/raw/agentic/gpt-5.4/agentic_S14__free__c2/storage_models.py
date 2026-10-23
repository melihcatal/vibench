from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional


def _to_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            if value.endswith("Z"):
                value = value[:-1] + "+00:00"
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None

    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: Optional[str] = None


@dataclass(slots=True)
class UploadObjectResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    checksum_sha256: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "key": self.key,
            "etag": self.etag,
            "version_id": self.version_id,
            "checksum_sha256": self.checksum_sha256,
        }


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int]
    etag: Optional[str]
    content_type: Optional[str]
    last_modified: Optional[datetime]
    metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None
    storage_class: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "key": self.key,
            "size": self.size,
            "etag": self.etag,
            "content_type": self.content_type,
            "last_modified": self.last_modified.astimezone(timezone.utc).isoformat() if self.last_modified else None,
            "metadata": dict(self.metadata),
            "version_id": self.version_id,
            "storage_class": self.storage_class,
        }


@dataclass(slots=True)
class ListedObject:
    key: str
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[datetime]
    storage_class: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "size": self.size,
            "etag": self.etag,
            "last_modified": self.last_modified.astimezone(timezone.utc).isoformat() if self.last_modified else None,
            "storage_class": self.storage_class,
        }


@dataclass(slots=True)
class OCRResult:
    text: str
    pages: int
    provider: str = "aws_textract"


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    source_language_code: Optional[str]
    target_language_code: str
    provider: str = "amazon_translate"


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider: str = "openai"


@dataclass(slots=True)
class EmbeddingResult:
    embedding: list[float]
    dimensions: int
    model: str
    provider: str = "openai"


def normalize_head_object(bucket: str, key: str, head: Mapping[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        size=head.get("ContentLength"),
        etag=head.get("ETag"),
        content_type=head.get("ContentType"),
        last_modified=_to_datetime(head.get("LastModified")),
        metadata=dict(head.get("Metadata", {}) or {}),
        version_id=head.get("VersionId"),
        storage_class=head.get("StorageClass"),
    )


def normalize_listed_object(item: Mapping[str, Any]) -> ListedObject:
    return ListedObject(
        key=str(item.get("Key", "")),
        size=item.get("Size"),
        etag=item.get("ETag"),
        last_modified=_to_datetime(item.get("LastModified")),
        storage_class=item.get("StorageClass"),
    )
