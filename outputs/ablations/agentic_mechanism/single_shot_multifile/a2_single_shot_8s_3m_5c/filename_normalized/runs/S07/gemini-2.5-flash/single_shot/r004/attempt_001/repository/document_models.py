from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocumentInput:
    document_bytes: bytes
    mime_type: str = "application/pdf"

@dataclass
class TextExtractionResult:
    text: str

@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

@dataclass
class LayoutBlock:
    text_content: Optional[str]
    block_type: str
    bounding_box: BoundingBox
    confidence: Optional[float] = None

@dataclass
class LayoutExtractionResult:
    blocks: List[LayoutBlock]
    full_text: Optional[str] = None

@dataclass
class TableCell:
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    bounding_box: Optional[BoundingBox] = None
    is_header: bool = False

@dataclass
class Table:
    cells: List[TableCell]
    bounding_box: Optional[BoundingBox] = None
    caption: Optional[str] = None

@dataclass
class TableExtractionResult:
    tables: List[Table]

@dataclass
class KeyValuePair:
    key: str
    value: str
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None
    confidence: Optional[float] = None

@dataclass
class KeyValueExtractionResult:
    key_value_pairs: List[KeyValuePair]

@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str = "en"

@dataclass
class SafetyRating:
    category: str
    score: float
    harmless: bool

@dataclass
class SafetyResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]

@dataclass
class FieldExtractionResult:
    extracted_fields: Dict[str, Any]

@dataclass
class EmbeddingResult:
    embedding: List[float]
    text: str