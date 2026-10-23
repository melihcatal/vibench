from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    image_bytes: Optional[bytes] = None
    url: Optional[str] = None
    path: Optional[str] = None
    content_type: Optional[str] = None


@dataclass
class DocumentRequest:
    source: DocumentSource
    language: Optional[str] = None
    features: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentTextResult:
    text: str
    confidence: Optional[float] = None
    provider: str = ""
    raw: Any = None


@dataclass
class DocumentLayoutElement:
    kind: str
    text: str = ""
    confidence: Optional[float] = None
    bbox: Optional[List[float]] = None
    page_number: Optional[int] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    raw: Any = None


@dataclass
class DocumentLayoutResult:
    elements: List[DocumentLayoutElement]
    provider: str = ""
    raw: Any = None


@dataclass
class DocumentTableCell:
    row_index: int
    column_index: int
    text: str = ""
    confidence: Optional[float] = None
    row_span: int = 1
    column_span: int = 1
    raw: Any = None


@dataclass
class DocumentTableResult:
    cells: List[DocumentTableCell]
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    provider: str = ""
    raw: Any = None


@dataclass
class DocumentKeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    raw: Any = None


@dataclass
class DocumentKeyValueResult:
    pairs: List[DocumentKeyValuePair]
    provider: str = ""
    raw: Any = None


@dataclass
class DocumentFieldResult:
    fields: Dict[str, Any]
    provider: str = ""
    raw: Any = None


@dataclass
class DocumentEmbeddingResult:
    vectors: List[List[float]]
    provider: str = ""
    raw: Any = None


@dataclass
class ModerationResult:
    unsafe: bool
    score: Optional[float] = None
    categories: Dict[str, float] = field(default_factory=dict)
    provider: str = ""
    raw: Any = None


@dataclass
class TranslationResult:
    translated_text: str
    provider: str = ""
    raw: Any = None


def normalize_text(text: Optional[str]) -> str:
    return " ".join((text or "").split())


def normalize_key(text: Optional[str]) -> str:
    return normalize_text(text).lower().strip().replace(":", "")
