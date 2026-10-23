from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class TextExtractionResponse(BaseModel):
    text: str
    pages: int
    language: Optional[str] = None


class LayoutElement(BaseModel):
    element_type: str
    text: str
    bounding_box: Optional[List[Dict[str, float]]] = None


class LayoutExtractionResponse(BaseModel):
    elements: List[LayoutElement]


class TableCell(BaseModel):
    row_index: int
    column_index: int
    text: str
    bounding_box: Optional[List[Dict[str, float]]] = None


class Table(BaseModel):
    rows: int
    columns: int
    cells: List[TableCell]


class TableExtractionResponse(BaseModel):
    tables: List[Table]


class KeyValuePair(BaseModel):
    key: Optional[str]
    value: Optional[str]
    confidence: Optional[float] = None


class KeyValueExtractionResponse(BaseModel):
    key_values: List[KeyValuePair]


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    unsafe_categories: List[str]
    confidence_scores: Dict[str, float]


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, Any]
    confidence_scores: Dict[str, float]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: str