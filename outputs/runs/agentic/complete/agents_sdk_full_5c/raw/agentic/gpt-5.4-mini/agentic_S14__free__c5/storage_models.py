from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ObjectUploadRequest:
    key: str
    body: bytes
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ObjectHeadResponse:
    bucket: str
    key: str
    etag: Optional[str]
    size: int
    last_modified: Optional[str]
    content_type: Optional[str]
    metadata: Dict[str, str]


@dataclass
class ListedObject:
    key: str
    size: int
    last_modified: Optional[str]
    etag: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class PresignedDownloadResponse:
    bucket: str
    key: str
    url: str
    expires_in: int


@dataclass
class TextExtractionResult:
    bucket: str
    key: str
    text: str
    language: Optional[str] = None
    provider: str = ""


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = ""


@dataclass
class AssetSummaryResult:
    source_key: str
    summary: str
    provider: str = ""


@dataclass
class EmbeddingResult:
    object_key: str
    metadata_vector: List[float]
    text_vector: List[float]
    provider: str = ""


def isoformat_utc(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def serialize_dataclass(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
