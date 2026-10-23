from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocumentExtractionRequest:
    document_bytes: bytes
    mime_type: str = "application/pdf"
    processor_id: Optional[str] = None
    location: str = "us"

@dataclass
class TextExtractionResponse:
    text: str

@dataclass
class LayoutExtractionResponse:
    pages: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class TableExtractionResponse:
    tables: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class KeyValueExtractionResponse:
    key_value_pairs: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class SafetyAnalysisRequest:
    text: str

@dataclass
class SafetyAnalysisResponse:
    categories: List[Dict[str, Any]] = field(default_factory=list)
    sentiment_score: float = 0.0

@dataclass
class FieldExtractionRequest:
    document_bytes: bytes
    mime_type: str = "application/pdf"
    processor_id: Optional[str] = None
    location: str = "us"

@dataclass
class FieldExtractionResponse:
    fields: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EmbeddingRequest:
    text_segments: List[str]

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]] = field(default_factory=list)
