from typing import List, Optional
from pydantic import BaseModel


class Block(BaseModel):
    content: str
    bounding_box: List[float]


class Line(BaseModel):
    content: str
    bounding_box: List[float]


class TableCell(BaseModel):
    row_index: int
    column_index: int
    content: str
    kind: Optional[str] = None


class Table(BaseModel):
    row_count: int
    column_count: int
    cells: List[TableCell]
    bounding_box: List[float]


class KeyValuePair(BaseModel):
    key: str
    value: Optional[str]
    confidence: float


class ExtractedLayout(BaseModel):
    blocks: List[Block]
    lines: List[Line]


class ExtractedText(BaseModel):
    content: str


class ExtractedTables(BaseModel):
    tables: List[Table]


class ExtractedKeyValues(BaseModel):
    key_values: List[KeyValuePair]
