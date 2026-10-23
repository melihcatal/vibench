from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    file_path: str
    mime_type: Optional[str] = None
    features: List[str] = field(default_factory=list)


@dataclass
class TextExtractionResult:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "google_document_ai"


@dataclass
class LayoutElement:
    kind: str
    text: str
    page: int
    bbox: List[float] = field(default_factory=list)
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
    header_rows: List[List[str]] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class KeyValueField:
    key: str
    value: str
    confidence: Optional[float] = None
    page: Optional[int] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    provider: str = "google_cloud_translate"


@dataclass
class SafetyResult:
    blocked: bool
    categories: Dict[str, float] = field(default_factory=dict)
    provider: str = "openai_moderations"


@dataclass
class StructuredFieldResult:
    fields: Dict[str, Any]
    provider: str = "openai_responses"


@dataclass
class EmbeddingResult:
    embeddings: List[List[float]]
    model: str
    provider: str = "openai_embeddings"


def get_text(anchor: Any, text: str) -> str:
    if not anchor or not getattr(anchor, "text_segments", None):
        return ""
    segments = []
    for segment in anchor.text_segments:
        start = int(segment.start_index) if getattr(segment, "start_index", None) is not None else 0
        end = int(segment.end_index) if getattr(segment, "end_index", None) is not None else len(text)
        segments.append(text[start:end])
    return "".join(segments).strip()


def normalize_polygon(bounding_poly: Any) -> List[float]:
    vertices = getattr(bounding_poly, "normalized_vertices", None) or getattr(bounding_poly, "vertices", None) or []
    coords: List[float] = []
    for v in vertices:
        x = float(getattr(v, "x", 0.0) or 0.0)
        y = float(getattr(v, "y", 0.0) or 0.0)
        coords.extend([x, y])
    return coords
