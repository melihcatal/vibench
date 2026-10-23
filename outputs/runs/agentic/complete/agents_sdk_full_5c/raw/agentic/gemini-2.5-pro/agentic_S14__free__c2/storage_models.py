from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class UploadResult:
    """Represents the result of a file upload operation."""
    bucket: str
    key: str
    e_tag: str
    version_id: Optional[str] = None

@dataclass
class ObjectMetadata:
    """Represents core metadata for a stored object."""
    key: str
    content_length: int
    content_type: str
    last_modified: str
    e_tag: str
    metadata: Dict[str, Any]

@dataclass
class ListedObject:
    """Represents a single object in a listing operation."""
    key: str
    size: int
    last_modified: str

@dataclass
class OcrResult:
    """Represents the result of an OCR operation."""
    source_uri: str
    text: str
    language: str

@dataclass
class TranslationResult:
    """Represents the result of a translation operation."""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class SummaryResult:
    """Represents the result of a summarization operation."""
    original_text: str
    summary: str
    model_used: str

@dataclass
class EmbeddingResult:
    """Represents the result of an embedding operation."""
    texts: List[str]
    embeddings: List[List[float]]
    model_used: str
