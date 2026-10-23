from typing import Dict, List, Optional
from pydantic import BaseModel


class BoundingBox(BaseModel):
    vertices: List[Dict[str, float]]


class TextBlock(BaseModel):
    text: str
    bounding_box: BoundingBox


class OCRResponse(BaseModel):
    text: str
    blocks: List[TextBlock]


class LayoutBlock(BaseModel):
    text: str
    bounding_box: BoundingBox
    block_type: str


class LayoutParagraph(BaseModel):
    text: str
    bounding_box: BoundingBox


class LayoutLine(BaseModel):
    text: str
    bounding_box: BoundingBox


class LayoutResponse(BaseModel):
    blocks: List[LayoutBlock]
    paragraphs: List[LayoutParagraph]
    lines: List[LayoutLine]


class TableCell(BaseModel):
    text: str
    bounding_box: BoundingBox


class TableRow(BaseModel):
    cells: List[TableCell]


class DocumentTable(BaseModel):
    rows: List[TableRow]
    bounding_box: BoundingBox


class TableResponse(BaseModel):
    tables: List[DocumentTable]


class KeyValuePair(BaseModel):
    key: str
    value: str
    key_bounding_box: Optional[BoundingBox]
    value_bounding_box: Optional[BoundingBox]


class KeyValueResponse(BaseModel):
    key_values: List[KeyValuePair]
