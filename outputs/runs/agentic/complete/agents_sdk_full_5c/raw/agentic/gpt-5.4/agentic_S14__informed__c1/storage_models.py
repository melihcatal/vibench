from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(slots=True)
class StorageLocation:
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
    content_type: Optional[str]
    size: Optional[int]


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str]
    size: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]
    metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass(slots=True)
class ListedObject:
    key: str
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[datetime]
    storage_class: Optional[str]


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    is_truncated: bool = False
    next_token: Optional[str] = None


@dataclass(slots=True)
class OCRResult:
    provider: str
    object_bucket: str
    object_key: str
    text: str
    page_count: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass(slots=True)
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str
    billed_characters: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass(slots=True)
class SummaryResult:
    provider: str
    model: str
    summary: str
    raw: Optional[Dict[str, Any]] = None


@dataclass(slots=True)
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int
    raw: Optional[Dict[str, Any]] = None


def normalize_metadata_map(metadata: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items()}


def join_text_parts(parts: Iterable[str]) -> str:
    return "\n".join(part.strip() for part in parts if part and part.strip())
