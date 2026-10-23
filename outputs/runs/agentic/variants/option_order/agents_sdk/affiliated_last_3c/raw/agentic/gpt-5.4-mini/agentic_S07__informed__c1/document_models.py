from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    source: str
    locale: Optional[str] = None


@dataclass
class OCRLine:
    text: str
    polygon: Optional[List[float]] = None
    confidence: Optional[float] = None


@dataclass
class OCRPage:
    page_number: int
    text: str
    lines: List[OCRLine] = field(default_factory=list)


@dataclass
class OCRResponse:
    text: str
    pages: List[OCRPage] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class LayoutBlock:
    block_type: str
    text: str
    page_number: Optional[int] = None
    polygon: Optional[List[float]] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1


@dataclass
class TableData:
    page_number: Optional[int]
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class NormalizedDocument:
    text: str
    lines: List[str] = field(default_factory=list)
    key_values: List[KeyValuePair] = field(default_factory=list)


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines() if line.strip())


def normalize_key_value_pairs(pairs: List[dict[str, Any]]) -> List[KeyValuePair]:
    normalized: List[KeyValuePair] = []
    for pair in pairs:
        normalized.append(
            KeyValuePair(
                key=str(pair.get("key", "")).strip(),
                value=str(pair.get("value", "")).strip(),
                confidence=pair.get("confidence"),
            )
        )
    return normalized
