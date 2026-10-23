from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DocumentTextExtractionResponse:
    text: str


@dataclass
class DocumentLayoutElement:
    type: str
    text: str
    bounding_boxes: List[List[int]]


@dataclass
class DocumentLayoutResponse:
    elements: List[DocumentLayoutElement]


@dataclass
class DocumentTableCell:
    row_index: int
    col_index: int
    text: str


@dataclass
class DocumentTable:
    cells: List[DocumentTableCell]
    num_rows: int
    num_columns: int


@dataclass
class DocumentTableExtractionResponse:
    tables: List[DocumentTable]


@dataclass
class DocumentKeyValueEntry:
    key: str
    value: str


@dataclass
class DocumentKeyValueExtractionResponse:
    key_values: List[DocumentKeyValueEntry]
