from pydantic import BaseModel
from typing import List, Dict, Any

class OCRText(BaseModel):
    text: str

class LayoutBlock(BaseModel):
    type: str
    text: str
    bounding_box: Dict[str, float]
    confidence: float = 0.0

class Table(BaseModel):
    rows: List[List[str]]
    bbox: Dict[str, float] = {}

class KeyValue(BaseModel):
    key: str
    value: str
    confidence: float = 0.0