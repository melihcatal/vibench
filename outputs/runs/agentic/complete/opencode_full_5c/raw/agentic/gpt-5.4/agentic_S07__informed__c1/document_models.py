from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/png"


@dataclass
class TextExtractionResult:
    provider: str
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Any] = None


@dataclass
class LayoutElement:
    element_type: str
    text: str
    page: int
    confidence: Optional[float] = None
    bbox: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutExtractionResult:
    provider: str
    elements: List[LayoutElement]
    raw: Optional[Any] = None


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
    raw: Optional[Any] = None


@dataclass
class KeyValueField:
    key: str
    value: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class KeyValueExtractionResult:
    provider: str
    fields: List[KeyValueField]
    raw: Optional[Any] = None


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Optional[Any] = None


@dataclass
class SafetyCheckResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    raw: Optional[Any] = None


@dataclass
class StructuredFieldExtractionResult:
    provider: str
    fields: Dict[str, Any]
    raw: Optional[Any] = None


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embeddings: List[List[float]]
    raw: Optional[Any] = None


def load_binary(source: DocumentSource) -> bytes:
    if source.image_bytes is not None:
        return source.image_bytes
    if source.image_path is None:
        raise ValueError("Either image_path or image_bytes must be provided")
    with open(source.image_path, "rb") as file:
        return file.read()


def polygon_to_bbox(polygon: Optional[List[Any]]) -> List[float]:
    if not polygon:
        return []
    xs: List[float] = []
    ys: List[float] = []
    for point in polygon:
        if isinstance(point, dict):
            xs.append(float(point.get("x", 0.0)))
            ys.append(float(point.get("y", 0.0)))
        else:
            xs.append(float(getattr(point, "x", 0.0)))
            ys.append(float(getattr(point, "y", 0.0)))
    return [min(xs), min(ys), max(xs), max(ys)]


def normalize_text(value: Optional[str]) -> str:
    return " ".join((value or "").split())


def group_table_cells(cells: List[TableCell]) -> List[List[str]]:
    if not cells:
        return []
    row_count = max(cell.row_index + cell.row_span for cell in cells)
    column_count = max(cell.column_index + cell.column_span for cell in cells)
    matrix = [["" for _ in range(column_count)] for _ in range(row_count)]
    for cell in cells:
        matrix[cell.row_index][cell.column_index] = cell.text
    return matrix
