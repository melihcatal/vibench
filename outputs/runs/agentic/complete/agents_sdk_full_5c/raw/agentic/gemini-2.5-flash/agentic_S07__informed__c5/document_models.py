from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class DocumentProcessingRequest:
    document_path: str
    mime_type: str

@dataclass
class DocumentTextExtractionResponse:
    text_content: str

@dataclass
class DocumentLayoutExtractionResponse:
    text_content: str
    paragraphs: List[Any] = field(default_factory=list)
    blocks: List[Any] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)

@dataclass
class DocumentTableExtractionResponse:
    tables: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class DocumentKeyValueExtractionResponse:
    key_value_pairs: Dict[str, str] = field(default_factory=dict)

@dataclass
class OcrTranslateRequest:
    text_content: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class OcrTranslateResponse:
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class OcrSafetyRequest:
    text_content: str

@dataclass
class OcrSafetyResponse:
    safety_scores: Dict[str, float] = field(default_factory=dict)

@dataclass
class DocumentFieldExtractionRequest:
    document_path: str
    mime_type: str
    processor_id: str # Specific processor for field extraction (e.g., invoice parser)

@dataclass
class DocumentFieldExtractionResponse:
    extracted_fields: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OcrEmbeddingRequest:
    text_content: str

@dataclass
class OcrEmbeddingResponse:
    embedding: List[float] = field(default_factory=list)
