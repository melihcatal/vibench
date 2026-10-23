from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class DocumentPage:
    page_number: int
    text: str
    blocks: List[Dict[str, Any]]

@dataclass
class DocumentLayout:
    page_number: int
    blocks: List[Dict[str, Any]]

@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    confidence: float

@dataclass
class DocumentTable:
    id: str
    cells: List[TableCell]
    rows: int
    columns: int

@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float

@dataclass
class ExtractionResult:
    document_pages: List[DocumentPage]
    document_tables: List[DocumentTable]
    key_values: List[KeyValue]

@dataclass
class OcrTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class OcrTranslateResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str

@dataclass
class OcrSafetyRequest:
    text: str
    language_code: str

@dataclass
class OcrSafetyResponse:
    sentiment: str
    sentiment_score: Dict[str, float]
    entities: List[Dict[str, Any]]
    key_phrases: List[Dict[str, Any]]
    document_moderation_labels: List[Dict[str, Any]]

@dataclass
class DocumentFieldExtractionRequest:
    text: str
    language_code: str

@dataclass
class DocumentFieldExtractionResponse:
    extracted_fields: List[Dict[str, Any]]

@dataclass
class OcrEmbeddingRequest:
    text: str

@dataclass
class OcrEmbeddingResponse:
    embedding: List[float]
