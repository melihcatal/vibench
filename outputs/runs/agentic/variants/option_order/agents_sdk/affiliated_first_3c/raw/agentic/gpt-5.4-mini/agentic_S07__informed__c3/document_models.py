from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    document_path: Optional[str] = None
    document_bytes: Optional[bytes] = None
    locale: Optional[str] = None


@dataclass
class OCRTextResponse:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Any] = None


@dataclass
class LayoutBlock:
    kind: str
    text: str
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LayoutResponse:
    blocks: List[LayoutBlock]
    raw: Optional[Any] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str


@dataclass
class TableResponse:
    rows: List[List[TableCell]]
    raw: Optional[Any] = None


@dataclass
class KeyValuePair:
    key: str
    value: str


@dataclass
class KeyValueResponse:
    pairs: List[KeyValuePair]
    raw: Optional[Any] = None


@dataclass
class NormalizedDocumentText:
    text: str
    lines: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: str) -> NormalizedDocumentText:
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    return NormalizedDocumentText(text="\n".join(lines), lines=lines)
