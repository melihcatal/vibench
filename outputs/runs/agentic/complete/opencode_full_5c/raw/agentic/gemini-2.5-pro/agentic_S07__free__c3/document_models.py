from typing import List, Optional
from pydantic import BaseModel, Field


class Word(BaseModel):
    content: str
    confidence: float
    polygon: List[float]


class Line(BaseModel):
    content: str
    confidence: float
    polygon: List[float]
    words: List[Word] = Field(default_factory=list)


class Block(BaseModel):
    content: str
    confidence: float
    polygon: List[float]
    lines: List[Line] = Field(default_factory=list)


class TableCell(BaseModel):
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    confidence: float
    polygon: List[float]


class TableRow(BaseModel):
    cells: List[TableCell] = Field(default_factory=list)


class Table(BaseModel):
    rows: List[TableRow] = Field(default_factory=list)
    row_count: int
    column_count: int
    confidence: float
    polygon: List[float]


class KeyValuePair(BaseModel):
    key: str
    key_polygon: List[float]
    value: Optional[str]
    value_polygon: Optional[List[float]]
    confidence: float


class DocumentLayout(BaseModel):
    blocks: List[Block] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    key_value_pairs: List[KeyValuePair] = Field(default_factory=list)
    full_text: Optional[str] = None
