from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class DocumentInput:
    content: bytes
    mime_type: str = "image/png"
    language_hints: List[str] = field(default_factory=list)
    filename: Optional[str] = None


@dataclass
class OCRTextResponse:
    text: str
    raw: Any = None


@dataclass
class LayoutBlock:
    kind: str
    text: str
    bounding_box: Optional[List[float]] = None
    raw: Any = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    raw: Any = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    raw: Any = None


@dataclass
class NormalizedDocument:
    text: str
    blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[List[TableCell]] = field(default_factory=list)
    key_values: List[KeyValuePair] = field(default_factory=list)
    raw: Any = None


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text.strip()
    if isinstance(text, (list, tuple)):
        return "\n".join(normalize_text(item) for item in text if normalize_text(item))
    return str(text).strip()


def normalize_blocks(raw_blocks: Iterable[Any]) -> List[LayoutBlock]:
    blocks: List[LayoutBlock] = []
    for block in raw_blocks or []:
        kind = normalize_text(_get_attr(block, "kind", _get_attr(block, "block_type", "block")))
        text = normalize_text(_get_attr(block, "text", _get_attr(block, "content", "")))
        bbox = _get_attr(block, "bounding_box", _get_attr(block, "bbox", None))
        blocks.append(LayoutBlock(kind=kind, text=text, bounding_box=bbox, raw=block))
    return blocks


def normalize_table_cells(raw_cells: Iterable[Any]) -> List[TableCell]:
    cells: List[TableCell] = []
    for cell in raw_cells or []:
        cells.append(
            TableCell(
                row_index=int(_get_attr(cell, "row_index", _get_attr(cell, "row", 0))),
                column_index=int(_get_attr(cell, "column_index", _get_attr(cell, "column", 0))),
                text=normalize_text(_get_attr(cell, "text", _get_attr(cell, "content", ""))),
                row_span=int(_get_attr(cell, "row_span", 1) or 1),
                column_span=int(_get_attr(cell, "column_span", 1) or 1),
                raw=cell,
            )
        )
    return cells


def normalize_key_values(raw_items: Iterable[Any]) -> List[KeyValuePair]:
    pairs: List[KeyValuePair] = []
    for item in raw_items or []:
        key = normalize_text(_get_attr(item, "key", _get_attr(item, "name", "")))
        value = normalize_text(_get_attr(item, "value", _get_attr(item, "text", "")))
        confidence = _get_attr(item, "confidence", None)
        pairs.append(KeyValuePair(key=key, value=value, confidence=confidence, raw=item))
    return pairs
