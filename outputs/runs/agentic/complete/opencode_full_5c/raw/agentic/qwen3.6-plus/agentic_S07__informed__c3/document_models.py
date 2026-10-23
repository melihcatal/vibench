from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class OCRTextResult:
    text: str
    confidence: float
    page_number: int


@dataclass
class LayoutBlock:
    content: str
    bounding_box: List[float]
    category: str
    confidence: float


@dataclass
class LayoutResult:
    blocks: List[LayoutBlock]
    page_width: float
    page_height: float


@dataclass
class TableCell:
    content: str
    row_index: int
    col_index: int
    row_span: int
    col_span: int


@dataclass
class TableResult:
    cells: List[TableCell]
    row_count: int
    col_count: int


@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float


@dataclass
class KeyValueResult:
    pairs: List[KeyValue]
