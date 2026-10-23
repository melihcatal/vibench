from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class TextExtractionResponse(BaseModel):
    text: str
    provider: str
    raw_response: Dict[str, Any]


class LayoutBlock(BaseModel):
    text: str
    bounding_box: List[Dict[str, float]]
    block_type: str  # e.g., "paragraph", "line", "word"


class LayoutExtractionResponse(BaseModel):
    blocks: List[LayoutBlock]
    provider: str
    raw_response: Dict[str, Any]


class TableCell(BaseModel):
    text: str
    row_index: int
    column_index: int
    bounding_box: List[Dict[str, float]]


class TableExtractionResponse(BaseModel):
    tables: List[Dict[str, List[TableCell]]]
    provider: str
    raw_response: Dict[str, Any]


class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: float


class KeyValueExtractionResponse(BaseModel):
    key_value_pairs: List[KeyValuePair]
    provider: str
    raw_response: Dict[str, Any]


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    raw_response: Dict[str, Any]


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    unsafe_categories: List[str]
    provider: str
    raw_response: Dict[str, Any]


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, str]
    provider: str
    raw_response: Dict[str, Any]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    provider: str
    raw_response: Dict[str, Any]