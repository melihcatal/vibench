from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class DocumentRequest:
    document_path: Optional[str] = None
    document_bytes: Optional[bytes] = None
    language_hint: Optional[str] = None
    mime_type: Optional[str] = None

    def validate(self) -> None:
        if not self.document_path and self.document_bytes is None:
            raise ValueError("document_path or document_bytes is required")


@dataclass
class OCRTextResponse:
    text: str
    provider: str = "azure-document-intelligence"
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    kind: str
    text: str
    bbox: Optional[List[float]] = None
    page: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResponse:
    elements: List[LayoutElement] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableResponse:
    cells: List[TableCell] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValueResponse:
    pairs: List[KeyValuePair] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"


@dataclass
class TranslationResponse:
    translated_text: str
    provider: str = "deepl"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResponse:
    unsafe: bool
    score: Optional[float] = None
    categories: Dict[str, float] = field(default_factory=dict)
    provider: str = "perspective-api"


@dataclass
class StructuredField:
    name: str
    value: Any
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredFieldResponse:
    fields: List[StructuredField] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResponse:
    vectors: List[List[float]] = field(default_factory=list)
    provider: str = "openai"
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def response_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)


def iter_nonempty_text(items: Iterable[Any]) -> List[str]:
    out: List[str] = []
    for item in items:
        text = getattr(item, "text", None)
        if text:
            out.append(normalize_whitespace(str(text)))
    return out
