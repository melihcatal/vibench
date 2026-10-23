from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    content: bytes
    mime_type: str
    filename: Optional[str] = None


@dataclass
class TextExtractionResult:
    provider: str
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    element_type: str
    text: str
    page: int
    confidence: Optional[float] = None
    bbox: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutExtractionResult:
    provider: str
    elements: List[LayoutElement]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    confidence: Optional[float] = None


@dataclass
class TableResult:
    page: int
    row_count: int
    column_count: int
    cells: List[TableCell]


@dataclass
class TableExtractionResult:
    provider: str
    tables: List[TableResult]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class KeyValueExtractionResult:
    provider: str
    items: List[KeyValueItem]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str
    source_language: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    provider: str
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldExtractionResult:
    provider: str
    fields: Dict[str, Any]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    vectors: List[List[float]]
    model: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def join_non_empty(parts: List[str], separator: str = "\n") -> str:
    return separator.join(part for part in parts if part)


def normalize_polygon(polygon: Any) -> Optional[List[float]]:
    if not polygon:
        return None
    if isinstance(polygon, list):
        normalized: List[float] = []
        for point in polygon:
            if isinstance(point, dict):
                normalized.extend(
                    [float(point.get("x", 0.0)), float(point.get("y", 0.0))]
                )
            elif isinstance(point, (list, tuple)) and len(point) >= 2:
                normalized.extend([float(point[0]), float(point[1])])
        return normalized or None
    return None
