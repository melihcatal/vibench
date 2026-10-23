from typing import List, Optional, Dict
from pydantic import BaseModel

class OCRTextResponse(BaseModel):
    text: str
    language: Optional[str] = None

class LayoutBlock(BaseModel):
    block_type: str
    text: str
    bounding_box: List[float]

class LayoutResponse(BaseModel):
    blocks: List[LayoutBlock]

class TableCell(BaseModel):
    row_index: int
    column_index: int
    text: str
    bounding_box: Optional[List[float]] = None

class TableResponse(BaseModel):
    row_count: int
    column_count: int
    cells: List[TableCell]

class KeyValueResponse(BaseModel):
    key: str
    value: str
    confidence: float