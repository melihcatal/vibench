from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from enum import Enum


class BlockType(Enum):
    LINE = "line"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    HEADING = "heading"
    LIST_ITEM = "list_item"


@dataclass
class TextExtractionRequest:
    image_path: str
    language_hints: Optional[List[str]] = None


@dataclass
class TextExtractionResponse:
    text: str
    confidence: float
    provider: str
    raw_response: Any


@dataclass
class LayoutExtractionRequest:
    document_path: str
    include_tables: bool = True
    include_lines: bool = True


@dataclass
class LayoutBlock:
    text: str
    bounding_box: Optional[List[Dict[str, float]]] = None
    type: str = "line"
    confidence: float = 0.9


@dataclass
class LayoutExtractionResponse:
    blocks: List[LayoutBlock]
    provider: str
    model_id: str
    raw_response: Any


@dataclass
class TableExtractionRequest:
    document_path: str
    max_tables: Optional[int] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    bounding_box: Optional[List[Dict[str, float]]] = None
    confidence: float = 0.9


@dataclass
class Table:
    table_index: int
    row_count: int
    column_count: int
    cells: List[TableCell]
    bounding_box: Optional[List[Dict[str, float]]] = None


@dataclass
class TableExtractionResponse:
    tables: List[Table]
    provider: str
    model_id: str
    raw_response: Any


@dataclass
class KeyValueExtractionRequest:
    document_path: str
    expected_fields: Optional[List[str]] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float
    bounding_box: Optional[List[Dict[str, float]]] = None


@dataclass
class KeyValueExtractionResponse:
    key_values: List[KeyValuePair]
    provider: str
    model_id: str
    raw_response: Any


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    raw_response: Any


@dataclass
class SafetyCheckRequest:
    text: str
    categories: Optional[List[str]] = None


@dataclass
class SafetyCategory:
    category: str
    score: float
    flagged: bool


@dataclass
class SafetyCheckResponse:
    categories: List[SafetyCategory]
    provider: str
    raw_response: Any


@dataclass
class FieldExtractionRequest:
    text: str
    field_schema: Dict[str, str]
    document_type: Optional[str] = None


@dataclass
class ExtractedField:
    name: str
    value: str
    confidence: float


@dataclass
class FieldExtractionResponse:
    fields: List[ExtractedField]
    provider: str
    model_id: str
    raw_response: Any


@dataclass
class EmbeddingRequest:
    text: str
    model: Optional[str] = None


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    provider: str
    model_id: str
    raw_response: Any
