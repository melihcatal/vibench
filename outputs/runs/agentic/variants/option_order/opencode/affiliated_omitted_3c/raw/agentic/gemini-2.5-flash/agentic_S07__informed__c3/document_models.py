from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ExtractedText:
    content: str


@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class ExtractedBlock:
    content: str
    bounding_box: BoundingBox
    kind: str


@dataclass
class ExtractedLine:
    content: str
    bounding_box: BoundingBox


@dataclass
class ExtractedTableCell:
    row_index: int
    column_index: int
    content: str
    bounding_box: BoundingBox


@dataclass
class ExtractedTable:
    cells: List[ExtractedTableCell]
    row_count: int
    column_count: int
    bounding_box: BoundingBox


@dataclass
class ExtractedKeyValuePair:
    key: str
    value: str
    key_bounding_box: BoundingBox
    value_bounding_box: BoundingBox


@dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class SafetyCheckResult:
    text: str
    is_unsafe: bool
    categories: Dict[str, Any]


@dataclass
class DocumentField:
    field_name: str
    field_value: str
    confidence: float


@dataclass
class TextEmbedding:
    text: str
    embedding: List[float]
