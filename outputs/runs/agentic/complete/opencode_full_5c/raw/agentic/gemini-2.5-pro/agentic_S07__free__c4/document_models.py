from dataclasses import dataclass, field
from typing import List


@dataclass
class Point:
    x: int
    y: int


@dataclass
class BoundingBox:
    vertices: List[Point] = field(default_factory=list)


@dataclass
class Word:
    text: str
    bounding_box: BoundingBox


@dataclass
class Line:
    text: str
    bounding_box: BoundingBox
    words: List[Word] = field(default_factory=list)


@dataclass
class Block:
    text: str
    bounding_box: BoundingBox
    lines: List[Line] = field(default_factory=list)


@dataclass
class TableCell:
    text: str
    row_index: int
    col_index: int
    bounding_box: BoundingBox


@dataclass
class TableRow:
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class Table:
    rows: List[TableRow] = field(default_factory=list)
    bounding_box: BoundingBox


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float


@dataclass
class DocumentLayout:
    text: str
    blocks: List[Block] = field(default_factory=list)
