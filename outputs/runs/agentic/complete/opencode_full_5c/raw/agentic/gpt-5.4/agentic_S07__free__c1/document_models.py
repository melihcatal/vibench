from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    source_path: Optional[str] = None
    source_url: Optional[str] = None
    mime_type: str = "application/octet-stream"
    language_hints: List[str] = field(default_factory=list)


@dataclass
class TextSpan:
    text: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class LayoutElement:
    element_type: str
    text: str
    page: Optional[int]
    confidence: Optional[float]
    bbox: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    confidence: Optional[float] = None


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class OCRTextResult:
    text: str
    spans: List[TextSpan] = field(default_factory=list)
    provider_payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResult:
    elements: List[LayoutElement]
    provider_payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableResult:
    cells: List[TableCell]
    rows: List[List[str]]
    provider_payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValueResult:
    items: List[KeyValueItem]
    provider_payload: Dict[str, Any] = field(default_factory=dict)


def load_bytes(request: DocumentRequest) -> bytes:
    if request.source_path:
        with open(request.source_path, "rb") as handle:
            return handle.read()
    raise ValueError("source_path is required for local document processing")


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def normalize_sections(text: str) -> List[str]:
    sections = [normalize_whitespace(part) for part in text.split("\n\n")]
    return [section for section in sections if section]


def as_plain_dict(items: List[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(item.__dict__.copy())
    return normalized
