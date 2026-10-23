import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class ExtractedText:
    text_content: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class BoundingPoly:
    vertices: List[Dict[str, float]]  # [{'x': 0.0, 'y': 0.0}, ...]


@dataclasses.dataclass
class LayoutElement:
    text_content: str
    bounding_box: BoundingPoly
    element_type: str  # e.g., 'paragraph', 'line', 'block'


@dataclasses.dataclass
class ExtractedLayout:
    layout_elements: List[LayoutElement]


@dataclasses.dataclass
class TableCell:
    text_content: str
    bounding_box: BoundingPoly
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1


@dataclasses.dataclass
class ExtractedTable:
    cells: List[TableCell]
    num_rows: int
    num_columns: int
    bounding_box: BoundingPoly
    text_content: str  # Raw text content of the table


@dataclasses.dataclass
class ExtractedTables:
    tables: List[ExtractedTable]


@dataclasses.dataclass
class KeyValuePair:
    key: str
    value: str
    key_bounding_box: BoundingPoly
    value_bounding_box: BoundingPoly


@dataclasses.dataclass
class ExtractedKeyValues:
    key_value_pairs: List[KeyValuePair]


@dataclasses.dataclass
class TranslatedText:
    translated_content: str
    detected_language_code: Optional[str] = None


@dataclasses.dataclass
class SafetyRating:
    category: str
    probability: str  # e.g., 'VERY_LIKELY', 'UNLIKELY'


@dataclasses.dataclass
class SafetyCheckResult:
    is_safe: bool
    safety_ratings: List[SafetyRating]


@dataclasses.dataclass
class DocumentField:
    field_name: str
    field_value: str
    field_bounding_box: Optional[BoundingPoly] = None
    value_bounding_box: Optional[BoundingPoly] = None


@dataclasses.dataclass
class DocumentFieldExtractionResult:
    fields: List[DocumentField]


@dataclasses.dataclass
class Embedding:
    values: List[float]


@dataclasses.dataclass
class DocumentSectionEmbedding:
    section_text: str
    embedding: Embedding
