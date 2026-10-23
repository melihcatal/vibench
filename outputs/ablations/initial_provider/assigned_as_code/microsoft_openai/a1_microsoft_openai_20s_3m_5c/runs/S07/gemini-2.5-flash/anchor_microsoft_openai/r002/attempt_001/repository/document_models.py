import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class AnalyzeDocumentRequest:
    document_bytes: bytes
    mime_type: str
    model_id: str

@dataclasses.dataclass
class DocumentLayout:
    pages: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    key_value_pairs: List[Dict[str, Any]]
    paragraphs: List[Dict[str, Any]]
    styles: List[Dict[str, Any]]
    languages: List[Dict[str, Any]]

@dataclasses.dataclass
class TranslatedText:
    text: str
    from_language: str
    to_language: str

@dataclasses.dataclass
class SafetyResult:
    is_safe: bool
    categories: Dict[str, Any]

@dataclasses.dataclass
class FieldExtractionResult:
    fields: Dict[str, Any]

@dataclasses.dataclass
class EmbeddingResult:
    embedding: List[float]
    text: str
