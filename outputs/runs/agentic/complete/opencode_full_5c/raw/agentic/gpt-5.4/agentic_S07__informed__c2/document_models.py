from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DocumentRequest:
    file_bytes: bytes
    filename: str | None = None
    mime_type: str | None = None
    locale: str | None = None
    model_id: str | None = None


@dataclass
class TextPage:
    page_number: int
    text: str
    width: float | None = None
    height: float | None = None


@dataclass
class TextExtractionResult:
    provider: str
    model_id: str
    content: str
    pages: list[TextPage] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    kind: str
    text: str
    page_number: int
    polygon: list[dict[str, float]] = field(default_factory=list)
    confidence: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutExtractionResult:
    provider: str
    model_id: str
    elements: list[LayoutElement] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    kind: str | None = None
    confidence: float | None = None


@dataclass
class TableResult:
    page_number: int
    row_count: int
    column_count: int
    cells: list[TableCell] = field(default_factory=list)


@dataclass
class TableExtractionResult:
    provider: str
    model_id: str
    tables: list[TableResult] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float | None = None
    page_number: int | None = None


@dataclass
class KeyValueExtractionResult:
    provider: str
    model_id: str
    pairs: list[KeyValuePair] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


def as_dict(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, dict):
        return {k: as_dict(v) for k, v in value.items()}
    if isinstance(value, list):
        return [as_dict(v) for v in value]
    if isinstance(value, tuple):
        return [as_dict(v) for v in value]
    return value


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return "\n".join(part.rstrip() for part in value.splitlines()).strip()


def polygon_to_dicts(polygon: Any) -> list[dict[str, float]]:
    points: list[dict[str, float]] = []
    if not polygon:
        return points
    for point in polygon:
        x = getattr(point, "x", None)
        y = getattr(point, "y", None)
        if x is None and isinstance(point, dict):
            x = point.get("x")
        if y is None and isinstance(point, dict):
            y = point.get("y")
        points.append({"x": float(x or 0.0), "y": float(y or 0.0)})
    return points
