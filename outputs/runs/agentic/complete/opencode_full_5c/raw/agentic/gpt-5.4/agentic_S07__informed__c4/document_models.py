from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_bytes: bytes
    mime_type: str
    model_id: Optional[str] = None
    language: Optional[str] = None


@dataclass
class TextExtractionResult:
    text: str
    provider: str
    raw: Any = None


@dataclass
class LayoutElement:
    kind: str
    text: str
    page: int
    bounding_polygon: List[Dict[str, float]] = field(default_factory=list)
    confidence: Optional[float] = None


@dataclass
class LayoutExtractionResult:
    text: str
    provider: str
    elements: List[LayoutElement]
    raw: Any = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1
    kind: str = "content"


@dataclass
class TableResult:
    page: int
    row_count: int
    column_count: int
    cells: List[TableCell]


@dataclass
class TablesExtractionResult:
    provider: str
    tables: List[TableResult]
    raw: Any = None


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class KeyValueExtractionResult:
    provider: str
    items: List[KeyValueItem]
    raw: Any = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str
    raw: Any = None


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    raw: Any = None


@dataclass
class StructuredField:
    name: str
    value: str
    confidence: Optional[float] = None


@dataclass
class FieldExtractionResult:
    provider: str
    fields: List[StructuredField]
    raw: Any = None


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embeddings: List[List[float]]
    raw: Any = None


def normalize_polygon(polygon: Any) -> List[Dict[str, float]]:
    points: List[Dict[str, float]] = []
    for point in polygon or []:
        x = getattr(point, "x", None)
        y = getattr(point, "y", None)
        if isinstance(point, dict):
            x = point.get("x", x)
            y = point.get("y", y)
        points.append({"x": float(x or 0.0), "y": float(y or 0.0)})
    return points


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()
