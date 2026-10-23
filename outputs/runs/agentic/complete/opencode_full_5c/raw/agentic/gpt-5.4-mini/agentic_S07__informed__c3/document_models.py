from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _getattr(obj: Any, name: str, default: Any = None) -> Any:
    return getattr(obj, name, default)


@dataclass
class OCRLine:
    content: str
    polygon: List[float] = field(default_factory=list)


@dataclass
class OCRResult:
    text: str
    lines: List[OCRLine] = field(default_factory=list)
    raw: Any = None


@dataclass
class LayoutBlock:
    kind: str
    content: str = ""
    raw: Any = None


@dataclass
class LayoutResult:
    blocks: List[LayoutBlock] = field(default_factory=list)
    raw: Any = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str


@dataclass
class TableResult:
    cells: List[TableCell] = field(default_factory=list)
    raw: Any = None


@dataclass
class KeyValueResult:
    pairs: Dict[str, str] = field(default_factory=dict)
    raw: Any = None


TablesResult = TableResult


def normalize_ocr_result(result: Any) -> OCRResult:
    lines = []
    text_parts = []
    for page in _getattr(result, "pages", []) or []:
        for line in _getattr(page, "lines", []) or []:
            content = _getattr(line, "content", "")
            if content:
                text_parts.append(content)
            lines.append(OCRLine(content=content, polygon=list(_getattr(line, "polygon", []) or [])))
    if not text_parts:
        text_parts = [
            _getattr(result, "content", "") or ""
        ]
    return OCRResult(text="
".join([p for p in text_parts if p]), lines=lines, raw=result)


def normalize_layout_result(result: Any) -> LayoutResult:
    blocks = []
    for block in _getattr(result, "paragraphs", []) or []:
        blocks.append(LayoutBlock(kind="paragraph", content=_getattr(block, "content", ""), raw=block))
    for table in _getattr(result, "tables", []) or []:
        blocks.append(LayoutBlock(kind="table", content=str(_getattr(table, "row_count", "")), raw=table))
    return LayoutResult(blocks=blocks, raw=result)


def normalize_tables_result(result: Any) -> TableResult:
    cells = []
    for table in _getattr(result, "tables", []) or []:
        for cell in _getattr(table, "cells", []) or []:
            cells.append(TableCell(row_index=int(_getattr(cell, "row_index", 0)), column_index=int(_getattr(cell, "column_index", 0)), content=_getattr(cell, "content", "")))
    return TableResult(cells=cells, raw=result)


def normalize_key_value_result(result: Any) -> KeyValueResult:
    pairs: Dict[str, str] = {}
    for kv in _getattr(result, "key_value_pairs", []) or []:
        key = _getattr(_getattr(kv, "key", None), "content", "")
        value = _getattr(_getattr(kv, "value", None), "content", "")
        if key:
            pairs[key] = value
    return KeyValueResult(pairs=pairs, raw=result)
