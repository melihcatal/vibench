from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TextExtractionResponse(BaseModel):
    full_text: str
    pages: List[Dict[str, Any]]
    provider: str
    model: str

class LayoutElement(BaseModel):
    element_type: str
    text: str
    bounding_box: Optional[List[float]]
    confidence: float

class LayoutExtractionResponse(BaseModel):
    elements: List[LayoutElement]
    provider: str
    model: str

class TableCell(BaseModel):
    row_index: int
    column_index: int
    text: str
    bounding_box: Optional[List[float]]
    confidence: float

class TableExtractionResponse(BaseModel):
    tables: List[Dict[str, Any]]
    provider: str
    model: str

class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: float

class KeyValueExtractionResponse(BaseModel):
    key_value_pairs: List[KeyValuePair]
    provider: str
    model: str