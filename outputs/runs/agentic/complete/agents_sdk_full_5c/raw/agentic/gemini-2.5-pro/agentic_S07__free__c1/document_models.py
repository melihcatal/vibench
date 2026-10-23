from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Point:
    x: float
    y: float

@dataclass
class BoundingBox:
    points: Tuple[Point, Point, Point, Point]

@dataclass
class TextBlock:
    content: str
    bounding_box: BoundingBox
    page_number: int

@dataclass
class TableCell:
    content: str
    row_index: int
    column_index: int
    bounding_box: BoundingBox
    kind: str = "content"

@dataclass
class Table:
    cells: List[TableCell]
    row_count: int
    column_count: int
    bounding_box: BoundingBox
    page_number: int

@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float
    bounding_box: BoundingBox
