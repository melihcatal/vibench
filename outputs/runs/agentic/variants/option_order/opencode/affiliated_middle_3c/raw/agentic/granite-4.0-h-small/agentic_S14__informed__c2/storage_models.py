from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


@dataclass(frozen=True)
class ObjectInfo:
    """Normalized metadata returned by upload or head operations."""

    bucket: str
    key: str
    size_bytes: int
    last_modified: datetime
    etag: str
    content_type: Optional[str] = None
    custom_metadata: Dict[str, Any] = dataclass.field(default_factory=dict)


@dataclass(frozen=True)
class ObjectVersion:
    """Versioning information when supported."""

    version_id: Optional[str] = None
    is_latest: bool = True


@dataclass(frozen=True)
class ListingItem:
    """Single item returned by list‑prefix operations."""

    key: str
    is_folder: bool  # folders are not real objects in B2, but a prefix ending with '/'
    size_bytes: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None


@dataclass(frozen=True)
class DownloadURL:
    url: str
    expires_at: datetime


@dataclass(frozen=True)
class UploadRequest:
    bucket: str
    key: str
    data: Optional[bytes] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None


@dataclass(frozen=True)
class OCRResult:
    text: str
    language: str = "en"
    confidence: float = 0.0


@dataclass(frozen=True)
class TranslationRequest:
    source_text: str
    target_lang: str
    source_lang: Optional[str] = None


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str
    detected_source_language: str
    confidence: float


@dataclass(frozen=True)
class AssetSummary:
    title: Optional[str] = None
    summary: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class EmbeddingVector:
    vector: List[float]
    model: str
    created_at: datetime
