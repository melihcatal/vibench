from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class TextExtractionResponse(BaseModel):
    text: str
    provider: str


class LayoutBlock(BaseModel):
    block_type: str
    text: str
    bounding_box: Dict[str, float]


class LayoutExtractionResponse(BaseModel):
    blocks: List[LayoutBlock]
    provider: str


class TableCell(BaseModel):
    row_index: int
    column_index: int
    text: str
    bounding_box: Dict[str, float]


class TableExtractionResponse(BaseModel):
    tables: List[Dict[str, List[TableCell]]]
    provider: str


class KeyValuePair(BaseModel):
    key: str
    value: str


class KeyValueExtractionResponse(BaseModel):
    key_values: List[KeyValuePair]
    provider: str


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    unsafe_categories: List[str]
    provider: str


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, str]
    provider: str


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    provider: str