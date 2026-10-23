from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class DocumentInput:
    document_url: Optional[str] = None
    document_bytes: Optional[bytes] = None
    content_type: Optional[str] = None  # e.g., "application/pdf", "image/jpeg"


@dataclass
class TextExtractionResult:
    text_content: str


@dataclass
class LayoutExtractionResult:
    blocks: List[Dict[str, Any]] = field(
        default_factory=list
    )  # List of dictionaries representing layout elements
    lines: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    key_value_pairs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class KeyValueExtractionResult:
    key_value_pairs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str


@dataclass
class ContentSafetyResult:
    is_safe: bool
    moderation_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldExtractionResult:
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    embedding: List[float]
    text: str
