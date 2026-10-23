from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, Optional


@dataclass(frozen=True)
class StorageObjectKey:
    bucket: str
    key: str


@dataclass(frozen=True)
class UploadRequest:
    bucket: str
    key: str
    content: bytes
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SignedUrlRequest:
    bucket: str
    key: str
    expires_in_seconds: int = 900


@dataclass(frozen=True)
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: Optional[str] = None


@dataclass(frozen=True)
class OcrRequest:
    bucket: str
    key: str
    language: Optional[str] = None


@dataclass(frozen=True)
class TranslationRequest:
    source_text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass(frozen=True)
class SummaryRequest:
    source_text: str
    max_sentences: int = 5


@dataclass(frozen=True)
class EmbeddingRequest:
    bucket: str
    key: str
    extracted_text: str = ""
    extra_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str] = None
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_head_response(bucket: str, key: str, response: Mapping[str, Any]) -> "ObjectMetadata":
        lm = response.get("LastModified")
        if lm is not None and getattr(lm, "tzinfo", None) is None:
            lm = lm.replace(tzinfo=timezone.utc)
        return ObjectMetadata(
            bucket=bucket,
            key=key,
            etag=response.get("ETag"),
            content_length=response.get("ContentLength"),
            content_type=response.get("ContentType"),
            last_modified=lm,
            metadata=dict(response.get("Metadata", {}) or {}),
        )


@dataclass(frozen=True)
class ListedObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str


@dataclass(frozen=True)
class SummaryResult:
    source_text: str
    summary: str


@dataclass(frozen=True)
class EmbeddingResult:
    bucket: str
    key: str
    vector: Iterable[float]
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
