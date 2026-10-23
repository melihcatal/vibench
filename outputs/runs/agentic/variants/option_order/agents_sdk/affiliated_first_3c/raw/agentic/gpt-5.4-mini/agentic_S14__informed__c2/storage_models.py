from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, Optional


@dataclass(frozen=True)
class StorageObjectRef:
    bucket: str
    key: str


@dataclass(frozen=True)
class UploadRequest:
    bucket: str
    key: str
    body: Any
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    acl: Optional[str] = None


@dataclass(frozen=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600


@dataclass(frozen=True)
class ObjectMetadataResponse:
    bucket: str
    key: str
    etag: Optional[str]
    size: Optional[int]
    last_modified: Optional[str]
    content_type: Optional[str]
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ListedObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None


@dataclass(frozen=True)
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[ListedObject]


@dataclass(frozen=True)
class OCRRequest:
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
    text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedDocument:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def isoformat_utc(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def normalize_metadata(mapping: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not mapping:
        return result
    for key, value in mapping.items():
        if value is None:
            continue
        result[str(key)] = str(value)
    return result


def compact_text(parts: Iterable[str]) -> str:
    return "\n".join(part.strip() for part in parts if part and part.strip())
