from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRTextResult:
    provider: str
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class LayoutElement:
    kind: str
    text: str
    page: int
    confidence: Optional[float] = None
    bbox: Optional[List[float]] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResult:
    provider: str
    elements: List[LayoutElement]
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    is_header: bool = False
    bbox: Optional[List[float]] = None


@dataclass
class TableResult:
    provider: str
    tables: List[Dict[str, Any]]
    raw: Optional[Dict[str, Any]] = None


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
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    categories: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class FieldExtractionResult:
    provider: str
    fields: Dict[str, Any]
    raw: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embeddings: List[List[float]]
    raw: Optional[Dict[str, Any]] = None


def flatten_azure_read_content(analyze_result: Dict[str, Any]) -> str:
    pages = analyze_result.get("pages", [])
    page_texts: List[str] = []
    for page in pages:
        lines = page.get("lines", [])
        page_text = "\n".join(line.get("content", "") for line in lines if line.get("content"))
        if page_text:
            page_texts.append(page_text)
    if page_texts:
        return "\n\n".join(page_texts)
    content = analyze_result.get("content")
    return content or ""


def polygon_to_bbox(polygon: Optional[List[float]]) -> Optional[List[float]]:
    if not polygon or len(polygon) < 8:
        return None
    xs = polygon[0::2]
    ys = polygon[1::2]
    return [min(xs), min(ys), max(xs), max(ys)]
