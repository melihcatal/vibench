import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class DocumentContent:
    content: bytes
    mime_type: str


@dataclasses.dataclass
class TextExtractionResult:
    text: str


@dataclasses.dataclass
class LayoutExtractionResult:
    pages: List[Dict[str, Any]]


@dataclasses.dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]]


@dataclasses.dataclass
class KeyValueExtractionResult:
    key_value_pairs: Dict[str, str]


@dataclasses.dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str


@dataclasses.dataclass
class SafetyCheckResult:
    attribute_scores: Dict[str, float]


@dataclasses.dataclass
class FieldExtractionResult:
    fields: Dict[str, Any]


@dataclasses.dataclass
class EmbeddingResult:
    embedding: List[float]
