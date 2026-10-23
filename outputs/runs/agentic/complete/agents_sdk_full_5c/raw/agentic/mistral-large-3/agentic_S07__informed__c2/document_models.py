from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class TextExtractionResponse(BaseModel):
    text: str
    pages: List[Dict[str, Any]]


class LayoutElement(BaseModel):
    text: str
    bounding_box: List[float]
    confidence: Optional[float] = None


class TableCell(BaseModel):
    row_index: int
    column_index: int
    text: str
    is_header: bool = False
    bounding_box: List[float]
    confidence: Optional[float] = None


class DocumentTable(BaseModel):
    row_count: int
    column_count: int
    cells: List[TableCell]


class LayoutExtractionResponse(BaseModel):
    paragraphs: List[LayoutElement]
    lines: List[LayoutElement]
    tables: List[DocumentTable]


class TableExtractionResponse(BaseModel):
    tables: List[DocumentTable]


class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: Optional[float] = None


class KeyValueExtractionResponse(BaseModel):
    key_values: List[KeyValuePair]


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, Any]


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    violations: List[str]
    confidence: Optional[float] = None


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: str