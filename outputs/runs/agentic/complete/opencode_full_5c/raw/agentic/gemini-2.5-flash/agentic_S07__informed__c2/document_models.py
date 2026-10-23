import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ExtractedText:
    text_content: str


@dataclasses.dataclass
class ExtractedLayoutElement:
    type: str  # e.g., 'block', 'line', 'table', 'form_field'
    text_content: str
    bounding_box: List[float]  # Normalized vertices [x1, y1, x2, y2, ...]


@dataclasses.dataclass
class ExtractedTable:
    table_content: str
    rows: List[List[str]]  # List of rows, each row is a list of cell contents
    bounding_box: List[float]


@dataclasses.dataclass
class ExtractedKeyValuePair:
    key: str
    value: str
    key_bounding_box: List[float]
    value_bounding_box: List[float]
