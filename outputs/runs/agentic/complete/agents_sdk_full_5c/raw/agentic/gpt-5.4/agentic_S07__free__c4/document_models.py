from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    file_path: str
    mime_type: str = "application/octet-stream"


@dataclass
class TextExtractionResult:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "google_document_ai"


@dataclass
class LayoutElement:
    element_type: str
    text: str
    page: int
    bbox: List[Dict[str, float]] = field(default_factory=list)
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


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
    header_rows: List[List[TableCell]] = field(default_factory=list)
    body_rows: List[List[TableCell]] = field(default_factory=list)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class NormalizedDocument:
    text: str
    blocks: List[LayoutElement] = field(default_factory=list)
    tables: List[TableResult] = field(default_factory=list)
    key_values: List[KeyValuePair] = field(default_factory=list)


def get_text_from_anchor(document: Any, text_anchor: Any) -> str:
    if not text_anchor or not getattr(text_anchor, "text_segments", None):
        return ""
    text = document.text or ""
    parts: List[str] = []
    for segment in text_anchor.text_segments:
        start = int(segment.start_index or 0)
        end = int(segment.end_index or 0)
        parts.append(text[start:end])
    return "".join(parts).strip()


def normalize_vertices(vertices: Any) -> List[Dict[str, float]]:
    normalized: List[Dict[str, float]] = []
    for v in vertices or []:
        normalized.append({"x": float(getattr(v, "x", 0.0)), "y": float(getattr(v, "y", 0.0))})
    return normalized
