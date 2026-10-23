from pydantic import BaseModel, Field
from typing import List, Optional


class BoundingBox(BaseModel):
    polygon: List[float]


class KeyValue(BaseModel):
    key: str
    value: Optional[str]
    confidence: float


class TableCell(BaseModel):
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1


class Table(BaseModel):
    cells: List[TableCell]
    row_count: int
    column_count: int


class DocumentLayout(BaseModel):
    bounding_box: BoundingBox
    content: str


class ExtractedDocument(BaseModel):
    text: str
    key_values: List[KeyValue] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    layout: List[DocumentLayout] = Field(default_factory=list)
