from typing import Dict, List, Optional
from pydantic import BaseModel


class BoundingBox(BaseModel):
    vertices: List[Dict[str, float]]


class Word(BaseModel):
    text: str
    confidence: float
    bounding_box: BoundingBox


class Paragraph(BaseModel):
    text: str
    confidence: float
    bounding_box: BoundingBox
    words: List[Word]


class Block(BaseModel):
    text: str
    confidence: float
    bounding_box: BoundingBox
    paragraphs: List[Paragraph]


class Page(BaseModel):
    blocks: List[Block]
    width: int
    height: int


class OCRResponse(BaseModel):
    full_text: str
    pages: List[Page]
    provider: str
    model: str


class LayoutElement(BaseModel):
    type: str
    text: str
    bounding_box: BoundingBox
    confidence: float
    children: List[Dict]


class LayoutResponse(BaseModel):
    layout_elements: List[Dict]
    provider: str
    model: str


class TableCell(BaseModel):
    text: str
    row_span: int
    col_span: int
    bounding_box: BoundingBox


class TableRow(BaseModel):
    cells: List[TableCell]
    bounding_box: BoundingBox


class Table(BaseModel):
    rows: List[TableRow]
    bounding_box: BoundingBox


class TableResponse(BaseModel):
    tables: List[Table]
    provider: str
    model: str


class KeyValuePair(BaseModel):
    key: str
    value: str
    key_bounding_box: Optional[BoundingBox]
    value_bounding_box: Optional[BoundingBox]
    confidence: float


class KeyValueResponse(BaseModel):
    key_values: List[KeyValuePair]
    provider: str
    model: str
