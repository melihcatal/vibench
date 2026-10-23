from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRBlock:
    text: str
    confidence: float = 0.0
    bounding_box: Optional[List[Dict[str, float]]] = None


@dataclass
class OCRResponse:
    text: str
    blocks: List[OCRBlock] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class LayoutElement:
    kind: str
    text: str
    confidence: float = 0.0
    bounding_box: Optional[List[Dict[str, float]]] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    confidence: float = 0.0


@dataclass
class TableResponse:
    cells: List[TableCell] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float = 0.0


@dataclass
class KeyValueResponse:
    pairs: List[KeyValuePair] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_document_ai_text(text: str) -> str:
    return normalize_text(text).strip()
