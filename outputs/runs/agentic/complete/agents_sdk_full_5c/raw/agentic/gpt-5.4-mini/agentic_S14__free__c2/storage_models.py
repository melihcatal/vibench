from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class ObjectInput:
    bucket: str
    key: str


@dataclass(frozen=True)
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]


@dataclass(frozen=True)
class MetadataResult:
    bucket: str
    key: str
    content_length: Optional[int]
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str]


@dataclass(frozen=True)
class ListedObject:
    key: str
    size: int
    last_modified: Optional[str]
    etag: Optional[str]


@dataclass(frozen=True)
class ListingResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    next_token: Optional[str]


@dataclass(frozen=True)
class SignedUrlResult:
    bucket: str
    key: str
    url: str
    expires_in_seconds: int


@dataclass(frozen=True)
class OcrResult:
    text: str
    language_code: Optional[str]
    confidence: Optional[float]


@dataclass(frozen=True)
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str


@dataclass(frozen=True)
class SummaryResult:
    summary: str
    source_length: int


@dataclass(frozen=True)
class EmbeddingResult:
    vector: List[float]
    dimension: int
    metadata: Dict[str, Any]


def normalize_text_chunks(chunks: Iterable[str]) -> str:
    return "\n".join(part.strip() for part in chunks if part and part.strip())
