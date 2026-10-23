from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ObjectRef:
    bucket: str
    key: str


@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListedObject:
    bucket: str
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class TextDocument:
    source: ObjectRef
    text: str
    language: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class SummaryResult:
    source: ObjectRef
    summary: str
    provider: Optional[str] = None


@dataclass
class EmbeddingResult:
    source: ObjectRef
    vector: List[float]
    dimension: int
    provider: Optional[str] = None


def normalize_datetime(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    return str(value)


def dataclass_to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)


def safe_join_text(parts: Iterable[str]) -> str:
    return "\n".join(part.strip() for part in parts if part and part.strip())
