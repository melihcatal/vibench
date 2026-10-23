from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class OCRTextResponse(BaseModel):
    text: str
    pages: List[Dict[str, Any]]


class LayoutElement(BaseModel):
    content: str
    bounding_box: Optional[List[float]]
    role: Optional[str] = None


class TableCell(BaseModel):
    content: str
    row_index: int
    column_index: int
    bounding_box: Optional[List[float]]


class TableResponse(BaseModel):
    row_count: int
    column_count: int
    cells: List[List[str]]
    bounding_box: Optional[List[float]]


class LayoutResponse(BaseModel):
    paragraphs: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    sections: List[Dict[str, Any]]


class KeyValueResponse(BaseModel):
    key: str
    value: str
    key_bounding_box: Optional[List[float]]
    value_bounding_box: Optional[List[float]]
    confidence: float


class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: str
    target_language: str


class SafetyResponse(BaseModel):
    is_safe: bool
    categories: Dict[str, float]
    blocklists_matched: List[str]


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, Any]
    confidence: float


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    section: str