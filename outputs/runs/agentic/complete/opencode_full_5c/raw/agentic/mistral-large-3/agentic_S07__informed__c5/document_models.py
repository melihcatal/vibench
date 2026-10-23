from typing import Dict, List, Optional, TypedDict
from pydantic import BaseModel


class BoundingBox(TypedDict):
    x1: float
    y1: float
    x2: float
    y2: float


class OCRTextBlock(BaseModel):
    text: str
    bounding_box: BoundingBox
    confidence: float


class OCRResponse(BaseModel):
    blocks: List[OCRTextBlock]
    full_text: str


class LayoutBlock(BaseModel):
    block_type: str  # "line", "word", "table", "form"
    bounding_box: BoundingBox
    confidence: float
    text: Optional[str] = None
    rows: Optional[List[Dict]] = None  # For tables


class KeyValuePair(BaseModel):
    key: OCRTextBlock
    value: OCRTextBlock
    confidence: float


class TableCell(BaseModel):
    text: str
    row_index: int
    col_index: int
    confidence: float
    bounding_box: BoundingBox


class TableStructure(BaseModel):
    rows: List[List[TableCell]]
    confidence: float
