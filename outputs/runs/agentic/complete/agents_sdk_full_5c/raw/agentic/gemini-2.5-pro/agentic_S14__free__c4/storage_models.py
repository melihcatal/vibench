from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
class ObjectMetadata:
    """Represents metadata for a stored object."""
    key: str
    version_id: Optional[str]
    size_bytes: int
    last_modified: datetime
    content_type: str
    etag: str
    custom_metadata: Dict[str, Any]

@dataclass
class PresignedUrl:
    """Represents a time-limited URL for object access."""
    key: str
    url: str
    method: str
    expires_at: datetime

@dataclass
class OcrResult:
    """Represents the extracted text from a document."""
    key: str
    text: str
    language: str

@dataclass
class TranslationResult:
    """Represents translated text."""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class SummaryResult:
    """Represents a summarized version of a text document."""
    id: str
    summary: str
    original_text_length: int
    summary_text_length: int

@dataclass
class EmbeddingVector:
    """Represents a document embedding."""
    model: str
    vector: List[float]
    total_tokens: int
