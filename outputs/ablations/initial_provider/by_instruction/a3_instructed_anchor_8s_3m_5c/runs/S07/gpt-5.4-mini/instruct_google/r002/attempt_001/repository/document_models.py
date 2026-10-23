from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    content: bytes
    mime_type: str


@dataclass
class TextResult:
    text: str


@dataclass
class LayoutElement:
    type: str
    text: str
    confidence: Optional[float] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str


@dataclass
class KeyValuePair:
    key: str
    value: str


def normalize_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def page_text_from_document(document: Any) -> str:
    text = getattr(document, "text", "") or ""
    return normalize_text(text)


def serialize_layout(elements: List[LayoutElement]) -> List[Dict[str, Any]]:
    return [{"type": e.type, "text": e.text, "confidence": e.confidence} for e in elements]
