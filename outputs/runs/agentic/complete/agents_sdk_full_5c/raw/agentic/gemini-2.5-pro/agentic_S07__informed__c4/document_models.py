from typing import List, Optional, Tuple, Any
from pydantic import BaseModel


class BoundingBox(BaseModel):
    polygon: List[Tuple[float, float]]
    page_number: int


class Paragraph(BaseModel):
    content: str
    role: Optional[str] = None
    bounding_regions: List[Any]  # Simplified for this example


class TableCell(BaseModel):
    row_index: int
    column_index: int
    content: str
    kind: Optional[str] = "content"


class Table(BaseModel):
    row_count: int
    column_count: int
    cells: List[TableCell]


class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: float
