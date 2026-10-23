from dataclasses import dataclass
from typing import Optional, List, Any


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float


@dataclass
class Line:
    text: str
    bounding_box: Optional[BoundingBox] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    row_span: int
    column_span: int
    content: str
    bounding_box: Optional[BoundingBox] = None


@dataclass
class Table:
    rows: int
    columns: int
    cells: List[TableCell]
    bounding_box: Optional[BoundingBox] = None


@dataclass
class LayoutBlock:
    block_type: str
    lines: List[Line]
    bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None
    confidence: float = 1.0


@dataclass
class DocumentExtractionResult:
    text: str
    layout_blocks: List[LayoutBlock]
    tables: List[Table]
    key_values: List[KeyValuePair]
    raw_response: Optional[Any] = None


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    confidence: Optional[float] = None


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: List[str]
    scores: dict[str, float]
    flagged_text: Optional[str] = None


@dataclass
class FieldExtractionResult:
    fields: dict[str, str]
    confidence_scores: dict[str, float]
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    text: str
    token_count: Optional[int] = None
