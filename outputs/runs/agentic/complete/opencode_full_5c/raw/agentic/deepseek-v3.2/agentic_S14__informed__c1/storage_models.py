from dataclasses import dataclass
from typing import Dict, Optional, Any
from datetime import datetime


@dataclass
class ObjectInfo:
    """Information about a stored object."""

    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str


@dataclass
class ObjectMetadata:
    """Metadata for a stored object."""

    bucket: str
    key: str
    size: int
    content_type: str
    last_modified: Optional[datetime]
    etag: str
    storage_class: str
    metadata: Dict[str, str]
    version_id: Optional[str] = None


@dataclass
class OCRResult:
    """Result from OCR processing."""

    text: str
    confidence: float
    pages: int
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    """Result from translation."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: Optional[float] = None


@dataclass
class SummaryResult:
    """Result from content summarization."""

    original_content: str
    summary: str
    model_id: str
    tokens_used: Optional[int] = None


@dataclass
class EmbeddingResult:
    """Result from embedding generation."""

    text: str
    embedding: list
    model_id: str
    dimensions: int
