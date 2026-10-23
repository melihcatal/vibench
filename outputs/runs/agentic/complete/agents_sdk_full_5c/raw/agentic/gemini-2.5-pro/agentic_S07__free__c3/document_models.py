from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Point:
    x: float
    y: float

@dataclass
class BoundingBox:
    points: List[Point]

@dataclass
class TextBlock:
    text: str
    bounding_box: BoundingBox
    confidence: float

@dataclass
class Line(TextBlock):
    pass

@dataclass
class TableCell:
    text: str
    row_index: int
    col_index: int
    row_span: int = 1
    col_span: int = 1

@dataclass
class Table:
    cells: List[TableCell]
    bounding_box: BoundingBox
    row_count: int
    column_count: int

@dataclass
class KeyValuePair:
    key: TextBlock
    value: TextBlock
    confidence: float
