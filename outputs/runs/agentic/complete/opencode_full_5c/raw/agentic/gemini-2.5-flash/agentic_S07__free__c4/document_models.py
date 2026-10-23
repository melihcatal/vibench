from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DocumentInput:
    content: bytes = field(default=None)
    gcs_source: str = field(default=None)
    mime_type: str = field(default=None)


@dataclass
class ExtractedText:
    text: str


@dataclass
class ExtractedLayout:
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    lines: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    form_fields: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExtractedTable:
    rows: List[List[Dict[str, Any]]] = field(default_factory=list)


@dataclass
class ExtractedKeyValue:
    key: str
    value: str


@dataclass
class TranslatedText:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SafetyAnnotation:
    category: str
    score: float


@dataclass
class DocumentField:
    field_name: str
    field_value: str
    confidence: float


@dataclass
class TextEmbedding:
    embedding: List[float]
