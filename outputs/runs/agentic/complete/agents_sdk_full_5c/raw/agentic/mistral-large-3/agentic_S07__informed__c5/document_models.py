from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum


class BlockType(Enum):
    WORD = "word"
    LINE = "line"
    PARAGRAPH = "paragraph"
    BLOCK = "block"
    TABLE = "table"
    CELL = "cell"
    KEY_VALUE = "key_value"


@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float


@dataclass
class DocumentElement:
    text: Optional[str] = None
    block_type: Optional[BlockType] = None
    bounding_box: Optional[BoundingBox] = None
    confidence: Optional[float] = None
    children: Optional[List['DocumentElement']] = None


@dataclass
class TableCell:
    row_index: int
    col_index: int
    row_span: int
    col_span: int
    text: str
    bounding_box: BoundingBox
    confidence: float


@dataclass
class DocumentTable:
    rows: int
    cols: int
    cells: List[TableCell]
    bounding_box: BoundingBox


@dataclass
class KeyValuePair:
    key: DocumentElement
    value: DocumentElement
    confidence: float


@dataclass
class DocumentLayout:
    elements: List[DocumentElement]
    tables: List[DocumentTable]
    key_value_pairs: List[KeyValuePair]


@dataclass
class DocumentText:
    full_text: str
    pages: List[str]
    confidence: float
