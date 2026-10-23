from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class StorageObjectRef:
    bucket: str
    key: str


@dataclass
class UploadRequest(StorageObjectRef):
    data: bytes | bytearray | memoryview | Any
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class SignedUrlRequest(StorageObjectRef):
    expires_in_seconds: int = 900


@dataclass
class HeadObjectResult(StorageObjectRef):
    etag: Optional[str] = None
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class ListedObject:
    bucket: str
    key: str
    size: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None


@dataclass
class OCRResult(StorageObjectRef):
    text: str = ""
    pages: List[str] = field(default_factory=list)


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class SummaryResult:
    source_text: str
    summary: str


@dataclass
class EmbeddingResult:
    text: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_metadata(metadata: Mapping[str, Any] | None) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items() if v is not None}


def normalize_text_parts(parts: Iterable[Any]) -> str:
    return "\n".join(str(p).strip() for p in parts if str(p).strip())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
