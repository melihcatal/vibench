from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    file_path: str
    mime_type: Optional[str] = None
    language_hints: List[str] = field(default_factory=list)


@dataclass
class TextExtractionResult:
    provider: str
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    kind: str
    text: str
    page: int
    bbox: List[float]
    confidence: Optional[float] = None
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
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class StructuredFieldResult:
    provider: str
    fields: Dict[str, Any]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vectors: List[List[float]]


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    categories: Dict[str, Any]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Optional[str]) -> str:
    return " ".join((value or "").split())


def load_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


def polygon_to_bbox(polygon: Any) -> List[float]:
    if not polygon:
        return []
    xs: List[float] = []
    ys: List[float] = []
    for point in polygon:
        x = getattr(point, "x", None)
        y = getattr(point, "y", None)
        if x is not None:
            xs.append(float(x))
        if y is not None:
            ys.append(float(y))
    if not xs or not ys:
        return []
    return [min(xs), min(ys), max(xs), max(ys)]
