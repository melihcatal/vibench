from typing import List, Optional
from pydantic import BaseModel


class DocumentTextBlock(BaseModel):
    content: str
    page_number: int


class DocumentLayoutBlock(BaseModel):
    content: str
    page_number: int
    bounding_box: List[float]


class DocumentTable(BaseModel):
    row_count: int
    column_count: int
    cells: List[dict]


class DocumentKeyValuePair(BaseModel):
    key: str
    value: Optional[str]
    confidence: float


class TranslatedText(BaseModel):
    text: str
    detected_source_lang: str


class SafetyResult(BaseModel):
    is_safe: bool
    violated_categories: List[str]


class ExtractedField(BaseModel):
    name: str
    value: Optional[str]
    confidence: float


class EmbeddingVector(BaseModel):
    embedding: List[float]
    model: str
