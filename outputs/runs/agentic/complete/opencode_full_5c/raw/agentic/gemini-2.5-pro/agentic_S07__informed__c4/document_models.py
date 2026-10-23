from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class Block:
    text: str
    confidence: float
    bounding_box: BoundingBox


@dataclass
class Line:
    text: str
    confidence: float
    bounding_box: BoundingBox


@dataclass
class Cell:
    text: str
    row_index: int
    column_index: int
    row_span: int
    column_span: int
    bounding_box: BoundingBox


@dataclass
class Table:
    rows: int
    columns: int
    cells: List[Cell]
    bounding_box: BoundingBox


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float


@dataclass
class DocumentLayout:
    text: str
    blocks: List[Block]
    lines: List[Line]
    tables: List[Table]


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class SafetyRequest:
    text: str


@dataclass
class SafetyResponse:
    is_safe: bool
    reason: Optional[str] = None


@dataclass
class FieldExtractionRequest:
    file_path: str


@dataclass
class FieldExtractionResponse:
    fields: dict


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
