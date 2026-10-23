from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    source_bytes: bytes
    mime_type: str
    filename: Optional[str] = None


@dataclass
class OCRTextResult:
    provider: str
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    element_type: str
    text: str
    page: int
    bbox: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResult:
    provider: str
    elements: List[LayoutElement]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    bbox: List[float] = field(default_factory=list)


@dataclass
class TableResult:
    provider: str
    page: int
    cells: List[TableCell]
    row_count: int
    column_count: int
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class KeyValueResult:
    provider: str
    pairs: List[KeyValuePair]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    return " ".join(str(value).split())


def normalize_bbox(polygon: Optional[List[Any]]) -> List[float]:
    if not polygon:
        return []
    xs: List[float] = []
    ys: List[float] = []
    for point in polygon:
        if isinstance(point, dict):
            x = point.get("x")
            y = point.get("y")
        else:
            x = getattr(point, "x", None)
            y = getattr(point, "y", None)
        if x is not None:
            xs.append(float(x))
        if y is not None:
            ys.append(float(y))
    if not xs or not ys:
        return []
    return [min(xs), min(ys), max(xs), max(ys)]
