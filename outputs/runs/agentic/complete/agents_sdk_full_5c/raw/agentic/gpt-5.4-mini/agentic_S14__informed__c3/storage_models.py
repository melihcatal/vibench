from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


@dataclass(slots=True)
class ObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass(slots=True)
class UploadRequest:
    bucket: str
    key: str
    body: bytes | str | Any
    content_type: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    extra_args: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PresignedUrlRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    version_id: Optional[str] = None


@dataclass(slots=True)
class PrefixListRequest:
    bucket: str
    prefix: str = ""
    max_items: Optional[int] = None
    continuation_token: Optional[str] = None


@dataclass(slots=True)
class StoredObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str] = None
    size: Optional[int] = None
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ObjectListing:
    bucket: str
    prefix: str
    objects: list[dict[str, Any]] = field(default_factory=list)
    common_prefixes: list[str] = field(default_factory=list)
    next_token: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class OCRRequest:
    bucket: str
    key: str
    language_hint: Optional[str] = None


@dataclass(slots=True)
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass(slots=True)
class SummaryRequest:
    text: str
    max_sentences: int = 5


@dataclass(slots=True)
class EmbeddingRequest:
    bucket: str
    key: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    extracted_text: str = ""


@dataclass(slots=True)
class NormalizedTextResult:
    text: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SummaryResult:
    summary: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    dimensions: int
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(value or {})


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)
