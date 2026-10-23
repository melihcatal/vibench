from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    source_uri: Optional[str] = None
    bytes_base64: Optional[str] = None
    mime_type: str = "image/png"

    def as_google_document(self) -> Dict[str, Any]:
        if self.source_uri:
            return {"gcsUri": self.source_uri, "mimeType": self.mime_type}
        if self.bytes_base64:
            return {"content": self.bytes_base64, "mimeType": self.mime_type}
        raise ValueError("Either source_uri or bytes_base64 is required")


@dataclass
class NormalizedTextBlock:
    text: str
    page: int
    block_type: str
    bbox: List[Dict[str, float]] = field(default_factory=list)


@dataclass
class OCRTextResult:
    text: str
    pages: int
    blocks: List[NormalizedTextBlock] = field(default_factory=list)


@dataclass
class LayoutElement:
    page: int
    element_type: str
    text: str
    confidence: float
    bbox: List[Dict[str, float]] = field(default_factory=list)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1


@dataclass
class TableResult:
    page: int
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float


def get_text_anchor_text(
    document: Dict[str, Any], text_anchor: Optional[Dict[str, Any]]
) -> str:
    if not text_anchor:
        return ""
    full_text = document.get("text", "")
    segments = text_anchor.get("textSegments", [])
    parts: List[str] = []
    for segment in segments:
        start = int(segment.get("startIndex", 0))
        end = int(segment.get("endIndex", 0))
        parts.append(full_text[start:end])
    return "".join(parts).strip()


def normalize_bbox(vertices: Optional[List[Dict[str, Any]]]) -> List[Dict[str, float]]:
    if not vertices:
        return []
    return [
        {"x": float(vertex.get("x", 0.0)), "y": float(vertex.get("y", 0.0))}
        for vertex in vertices
    ]
