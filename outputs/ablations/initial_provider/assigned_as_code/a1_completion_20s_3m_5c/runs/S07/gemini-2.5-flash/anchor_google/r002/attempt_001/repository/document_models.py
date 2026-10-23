from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class DocumentField:
    name: str
    value: str
    confidence: float = 0.0

@dataclass
class DocumentLayout:
    text_segments: List[Dict[str, Any]] = field(default_factory=list)
    pages: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class DocumentTable:
    header_rows: List[List[str]] = field(default_factory=list)
    body_rows: List[List[str]] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class DocumentKeyValue:
    key: str
    value: str
    confidence: float = 0.0

@dataclass
class OcrTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class OcrSafetyResult:
    category: str
    probability: float

@dataclass
class OcrEmbedding:
    text_segment: str
    embedding_vector: List[float]

@dataclass
class Document:
    text: Optional[str] = None
    layout: Optional[DocumentLayout] = None
    tables: List[DocumentTable] = field(default_factory=list)
    key_values: List[DocumentKeyValue] = field(default_factory=list)
    fields: List[DocumentField] = field(default_factory=list)
    translated_text: Optional[OcrTranslation] = None
    safety_results: List[OcrSafetyResult] = field(default_factory=list)
    embeddings: List[OcrEmbedding] = field(default_factory=list)
