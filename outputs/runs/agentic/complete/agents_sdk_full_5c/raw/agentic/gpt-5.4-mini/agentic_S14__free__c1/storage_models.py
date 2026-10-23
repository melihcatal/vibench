from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class StorageObjectInfo:
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OCRResult:
    object_key: str
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SummaryResult:
    object_key: str
    summary: str
    bullets: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EmbeddingDocument:
    object_key: str
    metadata_text: str
    extracted_text: str


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


def join_nonempty(parts: Iterable[Optional[str]]) -> str:
    return "\n".join(part for part in parts if part)


def dict_to_text(payload: Mapping[str, Any]) -> str:
    lines = []
    for key, value in payload.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)
