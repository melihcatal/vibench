from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    source: str
    mime_type: str = "image/png"


@dataclass
class TextExtractionResult:
    text: str
    language: Optional[str] = None
    provider: str = "google-document-ai"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    element_type: str
    text: str
    page: int
    confidence: Optional[float] = None
    bbox: Optional[List[float]] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    col_span: int = 1
    confidence: Optional[float] = None


@dataclass
class TableResult:
    page: int
    header_rows: List[List[str]]
    body_rows: List[List[str]]
    cells: List[TableCell]
    provider: str = "google-document-ai"


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class KeyValueResult:
    items: List[KeyValueItem]
    provider: str = "google-document-ai"
    raw: Dict[str, Any] = field(default_factory=dict)


def text_anchor_to_string(document: Any, text_anchor: Any) -> str:
    if not text_anchor or not getattr(text_anchor, "text_segments", None):
        return ""
    pieces: List[str] = []
    for segment in text_anchor.text_segments:
        start = int(segment.start_index) if getattr(segment, "start_index", None) is not None else 0
        end = int(segment.end_index)
        pieces.append(document.text[start:end])
    return "".join(pieces).strip()


def normalize_bbox(vertices: Any) -> List[float]:
    if not vertices:
        return []
    coords: List[float] = []
    for vertex in vertices:
        coords.extend([float(getattr(vertex, "x", 0.0)), float(getattr(vertex, "y", 0.0))])
    return coords
