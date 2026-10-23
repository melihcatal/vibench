from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class BoundingBox(BaseModel):
    vertices: List[Dict[str, float]]


class DocumentTextResponse(BaseModel):
    text: str
    pages: int
    language: Optional[str] = None
    provider: str
    model: str


class LayoutElement(BaseModel):
    element_type: str
    text: str
    bounding_box: BoundingBox
    confidence: float


class LayoutResponse(BaseModel):
    elements: List[LayoutElement]
    pages: int
    provider: str
    model: str


class TableCell(BaseModel):
    text: str
    row_span: int = 1
    col_span: int = 1
    confidence: float = 1.0


class TableRow(BaseModel):
    cells: List[TableCell]


class Table(BaseModel):
    rows: List[TableRow]
    bounding_box: BoundingBox
    confidence: float


class TableResponse(BaseModel):
    tables: List[Table]
    pages: int
    provider: str
    model: str


class KeyValuePair(BaseModel):
    key: str
    value: str
    key_bounding_box: BoundingBox
    value_bounding_box: BoundingBox
    confidence: float


class KeyValueResponse(BaseModel):
    key_value_pairs: List[KeyValuePair]
    pages: int
    provider: str
    model: str


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    model: str


class SafetyResponse(BaseModel):
    is_safe: bool
    unsafe_categories: List[str]
    confidence: float
    provider: str
    model: str


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, Any]
    confidence: float
    provider: str
    model: str


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    provider: str
    model: str
