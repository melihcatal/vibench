import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class DocumentExtractionRequest:
    content: bytes
    mime_type: str
    processor_id: str
    location: str = "us"  # Google Cloud Document AI location


@dataclasses.dataclass
class TextExtractionResponse:
    text: str


@dataclasses.dataclass
class LayoutExtractionResponse:
    pages: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]


@dataclasses.dataclass
class TableExtractionResponse:
    tables: List[Dict[str, Any]]


@dataclasses.dataclass
class KeyValueExtractionResponse:
    key_value_pairs: List[Dict[str, Any]]


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str


@dataclasses.dataclass
class SafetyCheckRequest:
    text: str


@dataclasses.dataclass
class SafetyCheckResponse:
    scores: Dict[str, float]


@dataclasses.dataclass
class FieldExtractionRequest:
    document_content: bytes
    mime_type: str


@dataclasses.dataclass
class FieldExtractionResponse:
    fields: Dict[str, Any]


@dataclasses.dataclass
class EmbeddingRequest:
    text_sections: List[str]


@dataclasses.dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
