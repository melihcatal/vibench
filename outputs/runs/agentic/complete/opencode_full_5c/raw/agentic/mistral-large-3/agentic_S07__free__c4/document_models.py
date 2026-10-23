from typing import Dict, List, Optional
from pydantic import BaseModel


class BoundingBox(BaseModel):
    vertices: List[Dict[str, float]]


class Block(BaseModel):
    block_text: str
    bounding_box: BoundingBox


class Page(BaseModel):
    page_number: int
    blocks: List[Block]


class OCRResponse(BaseModel):
    provider: str
    text: str
    pages: List[Page]


class LayoutBlock(BaseModel):
    block_type: str
    text: str
    bounding_box: BoundingBox
    paragraphs: List[Dict]


class LayoutResponse(BaseModel):
    provider: str
    blocks: List[LayoutBlock]


class TableCell(BaseModel):
    text: str
    row_index: int
    column_index: int
    bounding_box: BoundingBox


class TableRow(BaseModel):
    cells: List[TableCell]


class Table(BaseModel):
    rows: List[TableRow]
    bounding_box: BoundingBox


class TableResponse(BaseModel):
    provider: str
    tables: List[Table]


class KeyValuePair(BaseModel):
    key: str
    value: str
    key_bounding_box: BoundingBox
    value_bounding_box: BoundingBox


class KeyValueResponse(BaseModel):
    provider: str
    key_value_pairs: List[KeyValuePair]
