from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentPageRange:
    first_page_number: int
    last_page_number: int


@dataclass
class TextSpan:
    content: str
    page_number: int
    polygon: List[Dict[str, float]] = field(default_factory=list)
    confidence: Optional[float] = None


@dataclass
class LayoutElement:
    kind: str
    content: str
    page_number: int
    polygon: List[Dict[str, float]] = field(default_factory=list)
    row_index: Optional[int] = None
    column_index: Optional[int] = None
    confidence: Optional[float] = None


@dataclass
class KeyValueElement:
    key: str
    value: str
    page_number: int
    key_polygon: List[Dict[str, float]] = field(default_factory=list)
    value_polygon: List[Dict[str, float]] = field(default_factory=list)
    confidence: Optional[float] = None


@dataclass
class NormalizedDocument:
    text: str
    pages: List[Dict[str, Any]]
    elements: List[LayoutElement] = field(default_factory=list)
    key_values: List[KeyValueElement] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def polygon_to_dicts(polygon: Optional[List[Any]]) -> List[Dict[str, float]]:
    if not polygon:
        return []
    points: List[Dict[str, float]] = []
    for point in polygon:
        x = getattr(point, "x", None)
        y = getattr(point, "y", None)
        if x is None and isinstance(point, dict):
            x = point.get("x")
        if y is None and isinstance(point, dict):
            y = point.get("y")
        if x is not None and y is not None:
            points.append({"x": float(x), "y": float(y)})
    return points


def normalize_whitespace(value: str) -> str:
    return " ".join((value or "").split())


def join_lines(lines: List[str]) -> str:
    return "\n".join([normalize_whitespace(line) for line in lines if normalize_whitespace(line)])
