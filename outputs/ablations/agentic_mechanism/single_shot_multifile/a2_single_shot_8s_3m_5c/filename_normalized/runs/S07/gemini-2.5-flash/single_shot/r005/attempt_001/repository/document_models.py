from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocumentTextResponse:
    text: str

@dataclass
class BoundingBox:
    x: int
    y: int

@dataclass
class LayoutBlock:
    text: str
    bounding_box: List[BoundingBox]

@dataclass
class DocumentLayoutResponse:
    blocks: List[LayoutBlock]

@dataclass
class TableCell:
    text: str
    row_span: int = 1
    col_span: int = 1

@dataclass
class DocumentTable:
    header_rows: List[List[TableCell]] = field(default_factory=list)
    body_rows: List[List[TableCell]] = field(default_factory=list)

@dataclass
class DocumentKeyValue:
    key: str
    value: str

@dataclass
class TranslationResponse:
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclass
class SafetyAttribute:
    category: str
    score: float
    severity: Optional[float] = None

@dataclass
class SafetyCheckResponse:
    is_safe: bool
    safety_attributes: List[SafetyAttribute]
    raw_response: Optional[Dict[str, Any]] = None

@dataclass
class FieldExtractionResponse:
    extracted_fields: Dict[str, Any]

@dataclass
class EmbeddingResponse:
    embeddings: List[float]
