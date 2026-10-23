from pydantic import BaseModel, Field
from typing import List, Optional

class Point(BaseModel):
    x: int
    y: int

class BoundingPoly(BaseModel):
    vertices: List[Point]

class LayoutElement(BaseModel):
    text: str
    bounding_poly: BoundingPoly
    confidence: float

class Line(LayoutElement):
    pass

class Block(LayoutElement):
    lines: List[Line]

class TableCell(LayoutElement):
    row_index: int
    col_index: int
    row_span: int = 1
    col_span: int = 1

class TableRow(BaseModel):
    cells: List[TableCell]

class Table(LayoutElement):
    header_rows: List[TableRow]
    body_rows: List[TableRow]

class KeyValuePair(BaseModel):
    key: str
    key_confidence: float
    value: str
    value_confidence: float

class ExtractedDocument(BaseModel):
    full_text: Optional[str] = None
    blocks: List[Block] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    key_value_pairs: List[KeyValuePair] = Field(default_factory=list)
