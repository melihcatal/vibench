from dataclasses import dataclass, field
from typing import List

@dataclass
class BoundingBox:
    top: float = 0.0
    left: float = 0.0
    width: float = 0.0
    height: float = 0.0

@dataclass
class LayoutElement:
    type: str
    bbox: BoundingBox
    text: str = ""
    confidence: float = 1.0
    children: List['LayoutElement'] = field(default_factory=list)

@dataclass
class TableRow:
    cells: List[str]

@dataclass
class Table:
    rows: List[TableRow]
    bbox: BoundingBox

@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float = 1.0
