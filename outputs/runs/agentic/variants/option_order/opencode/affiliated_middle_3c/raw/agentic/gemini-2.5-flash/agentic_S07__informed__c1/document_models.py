from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DocumentText:
    text: str


@dataclass
class LayoutBlock:
    text: str
    bounding_boxes: List[float]
    block_type: str


@dataclass
class TableCell:
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1


@dataclass
class Table:
    cells: List[TableCell]
    rows: int
    columns: int


@dataclass
class KeyValuePair:
    key: str
    value: str


@dataclass
class DocumentField:
    field_name: str
    field_value: str
    confidence: float


@dataclass
class OCREmbedding:
    text: str
    embedding: List[float]
