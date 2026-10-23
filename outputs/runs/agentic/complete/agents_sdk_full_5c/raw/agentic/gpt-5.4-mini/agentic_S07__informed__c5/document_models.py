from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class OCRTextResponse:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LayoutElement:
    kind: str
    content: str
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)
    confidence: Optional[float] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1


@dataclass
class TableResponse:
    rows: List[List[str]]
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class KeyValueResponse:
    pairs: List[KeyValuePair]


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return " ".join(_stringify(v) for v in value if _stringify(v))
    if isinstance(value, dict):
        return " ".join(_stringify(v) for v in value.values() if _stringify(v))
    text = getattr(value, "content", None)
    if isinstance(text, str):
        return text.strip()
    return str(value).strip()


def normalize_lines(lines: Iterable[Any]) -> List[str]:
    result: List[str] = []
    for line in lines:
        content = _stringify(getattr(line, "content", line))
        if content:
            result.append(content)
    return result


def normalize_key_values(pairs: Iterable[Any]) -> KeyValueResponse:
    normalized: List[KeyValuePair] = []
    for pair in pairs:
        key = _stringify(getattr(getattr(pair, "key", None), "content", getattr(pair, "key", "")))
        value = _stringify(getattr(getattr(pair, "value", None), "content", getattr(pair, "value", "")))
        if key or value:
            normalized.append(KeyValuePair(key=key, value=value, confidence=getattr(pair, "confidence", None)))
    return KeyValueResponse(pairs=normalized)
