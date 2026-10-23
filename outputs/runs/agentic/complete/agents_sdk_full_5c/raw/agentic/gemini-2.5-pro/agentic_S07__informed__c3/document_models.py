from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    polygon: List[float]

class DocumentElement(BaseModel):
    content: str
    bounding_box: BoundingBox

class Block(DocumentElement):
    role: Optional[str] = None

class Line(DocumentElement):
    pass

class TableCell(DocumentElement):
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    kind: str

class Table(BaseModel):
    cells: List[TableCell]
    row_count: int
    column_count: int

class KeyValuePair(BaseModel):
    key: DocumentElement
    value: Optional[DocumentElement] = None
    confidence: float
