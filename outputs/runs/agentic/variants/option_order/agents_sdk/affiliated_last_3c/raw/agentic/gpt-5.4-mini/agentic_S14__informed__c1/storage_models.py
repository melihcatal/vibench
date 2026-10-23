from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class StoredObjectReference:
    bucket: str
    key: str


@dataclass(frozen=True)
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass(frozen=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int]
    last_modified: Optional[str]
    content_type: Optional[str]
    etag: Optional[str]
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class ListedObject:
    key: str
    size: int
    last_modified: Optional[str]
    etag: Optional[str]
    storage_class: Optional[str]


@dataclass(frozen=True)
class OCRText:
    text: str
    raw: Dict[str, Any]


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str]
    target_language: str
    raw: Dict[str, Any]


@dataclass(frozen=True)
class SummaryResult:
    source_text: str
    summary: str
    raw: Dict[str, Any]


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    vector: List[float]
    raw: Dict[str, Any]


def normalize_s3_metadata(head_response: Dict[str, Any], bucket: str, key: str) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        size=head_response.get("ContentLength"),
        last_modified=str(head_response.get("LastModified")) if head_response.get("LastModified") else None,
        content_type=head_response.get("ContentType"),
        etag=head_response.get("ETag"),
        metadata=head_response.get("Metadata", {}),
    )
