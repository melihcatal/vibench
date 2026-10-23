from typing import List, Optional
from pydantic import BaseModel


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Word(BaseModel):
    text: str
    confidence: float
    bounding_box: BoundingBox


class Line(BaseModel):
    text: str
    words: List[Word]
    bounding_box: BoundingBox


class Block(BaseModel):
    text: str
    lines: List[Line]
    bounding_box: BoundingBox
    block_type: str  # E.g., 'TEXT', 'TABLE', 'PICTURE'


class TableCell(BaseModel):
    text: str
    row_span: int = 1
    col_span: int = 1
    bounding_box: BoundingBox


class TableRow(BaseModel):
    cells: List[TableCell]


class Table(BaseModel):
    rows: List[TableRow]
    bounding_box: BoundingBox


class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: float


class DocumentLayout(BaseModel):
    text: str
    blocks: List[Block]
    tables: List[Table]
    key_value_pairs: List[KeyValuePair]


class ImageAnalysisRequest(BaseModel):
    image_path: str
