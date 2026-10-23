from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class DocumentPayload:
    document_bytes: bytes
    mime_type: str


@dataclass
class DocumentConfig:
    project_id: str
    location: str
    processor_id: str = ""
    model_id: str = ""
    endpoint: str = ""


@dataclass
class TextExtractionResult:
    text: str


@dataclass
class LayoutExtractionResult:
    text: str
    pages: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]


@dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]]


@dataclass
class KeyValueExtractionResult:
    key_value_pairs: List[Dict[str, Any]]


@dataclass
class TranslationResult:
    translated_text: str
    detected_language_code: Optional[str] = None


@dataclass
class SafetyResult:
    safety_ratings: List[Dict[str, Any]]


@dataclass
class FieldExtractionResult:
    fields: Dict[str, Any]


@dataclass
class EmbeddingResult:
    embeddings: List[List[float]]
