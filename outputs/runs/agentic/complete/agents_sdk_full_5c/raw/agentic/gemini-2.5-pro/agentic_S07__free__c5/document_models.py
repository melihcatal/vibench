# document_models.py
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ExtractedText:
    content: str
    source_url: str

@dataclass
class BoundingBox:
    points: List[Dict[str, float]]

@dataclass
class LayoutElement:
    type: str
    content: str
    bounding_box: BoundingBox

@dataclass
class ExtractedLayout:
    elements: List[LayoutElement]
    source_url: str

@dataclass
class TableCell:
    content: str
    row_index: int
    column_index: int
    is_header: bool = False

@dataclass
class ExtractedTable:
    cells: List[TableCell]
    row_count: int
    column_count: int

@dataclass
class ExtractedKeyValuePair:
    key: str
    value: str
    confidence: float

@dataclass
class TranslationResponse:
    translated_text: str
    detected_language_code: str

@dataclass
class SafetyRating:
    category: str
    is_flagged: bool
    score: float

@dataclass
class ExtractedFields:
    data: Dict[str, Any]
