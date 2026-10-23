from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    path: Optional[str] = None
    url: Optional[str] = None
    mime_type: str = "application/octet-stream"


@dataclass
class TextSpan:
    text: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class LayoutElement:
    kind: str
    text: str = ""
    page: Optional[int] = None
    confidence: Optional[float] = None
    polygon: List[Dict[str, float]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class OCRResult:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    spans: List[TextSpan] = field(default_factory=list)
    provider: str = ""
    raw: Any = None


@dataclass
class LayoutResult:
    elements: List[LayoutElement]
    provider: str = ""
    raw: Any = None


@dataclass
class TableResult:
    tables: List[List[TableCell]]
    provider: str = ""
    raw: Any = None


@dataclass
class KeyValueResult:
    items: List[KeyValueItem]
    provider: str = ""
    raw: Any = None


def normalize_text(value: Optional[str]) -> str:
    return (value or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def polygon_to_dicts(polygon: Any) -> List[Dict[str, float]]:
    points: List[Dict[str, float]] = []
    for point in polygon or []:
        x = getattr(point, "x", None)
        y = getattr(point, "y", None)
        if x is None and isinstance(point, dict):
            x = point.get("x")
            y = point.get("y")
        if x is not None and y is not None:
            points.append({"x": float(x), "y": float(y)})
    return points


def coalesce_text(parts: List[str]) -> str:
    return "\n".join(part for part in (normalize_text(p) for p in parts) if part)
