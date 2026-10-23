from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ObjectLocation:
    bucket: str
    key: str


@dataclass
class UploadRequest(ObjectLocation):
    body: Any
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class PresignedDownloadRequest(ObjectLocation):
    expires_in: int = 3600


@dataclass
class PrefixListRequest:
    bucket: str
    prefix: str = ""
    max_results: Optional[int] = None


@dataclass
class TextTranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"


@dataclass
class SummaryRequest:
    text: str
    max_output_tokens: int = 256


@dataclass
class EmbeddingRequest:
    text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class OCRResult:
    text: str
    raw: Any = None


@dataclass
class TranslationResult:
    text: str
    raw: Any = None


@dataclass
class SummaryResult:
    summary: str
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    raw: Any = None


@dataclass
class ListedObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class ObjectListResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    raw: Any = None


def normalize_datetime(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        dt = value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    return str(value)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def coerce_float_vector(values: Iterable[Any]) -> List[float]:
    return [float(v) for v in values]
