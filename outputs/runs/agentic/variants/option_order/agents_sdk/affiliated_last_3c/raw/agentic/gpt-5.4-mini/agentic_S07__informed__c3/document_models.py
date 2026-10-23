from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    content: bytes
    mime_type: str = "image/png"
    language_hints: List[str] = field(default_factory=list)


@dataclass
class OCRTextResult:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    confidence: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class LayoutBlock:
    type: str
    text: str
    bbox: Optional[List[float]] = None
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
class TableResult:
    cells: List[TableCell] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class DocumentExtractionResult:
    items: List[Any] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


def normalize_text(text: Optional[str]) -> str:
    return " ".join((text or "").split())


def normalize_pairs(pairs: List[KeyValuePair]) -> List[KeyValuePair]:
    return [KeyValuePair(key=normalize_text(p.key), value=normalize_text(p.value), confidence=p.confidence) for p in pairs]
