from dataclasses import dataclass
from typing import Optional, List, Any

# Service identifiers:
# Provider: Google Document AI (Response normalization models)

@dataclass
class DocumentInfo:
    uri: Optional[str] = None  # e.g., gs://bucket/file.jpg
    mime_type: Optional[str] = 'application/pdf'
    binary_content: Optional[bytes] = None  # raw image or pdf bytes
    processor_id: Optional[str] = None  # OCR processor ID

@dataclass
class OcrResponse:
    text: str = ''
    confidence: float = 0.0
    bounding_poly: Optional[List[Any]] = None

@dataclass
class TableResponse:
    rows: List[List[str]] = dataclass.field(default_factory=list)
    confidence: float = 0.0
    bounding_poly: Optional[List[Any]] = None

@dataclass
class KvResponse:
    entries: List[dict] = dataclass.field(default_factory=list)
    confidence: float = 0.0

# Simple mapping from provider-specific types to neutral internal models for downstream steps
