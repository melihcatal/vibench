from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

@dataclass
class ObjectMetadata:
    """A normalized data class for object metadata."""
    name: str
    bucket: str
    size: int
    updated: datetime
    content_type: Optional[str] = None
    custom_metadata: Optional[Dict[str, str]] = None

@dataclass
class PresignedUrlResponse:
    """A data class for a presigned URL response."""
    object_name: str
    url: str
    expiration: datetime

@dataclass
class OcrResult:
    """Represents the extracted text from a document."""
    source_uri: str
    text: str

@dataclass
class TranslationResult:
    """Represents a translation result."""
    original_text: str
    translated_text: str
    target_language: str

@dataclass
class SummaryResult:
    """Represents a summarization result."""
    id: str
    summary: str
    source_text: str
    model: str

@dataclass
class EmbeddingResult:
    """Represents a text embedding result."""
    model: str
    embedding: List[float]
    source_text: str
