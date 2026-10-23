from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    file_path: str
    model_id: str = "prebuilt-layout"
    locale: Optional[str] = None
    pages: Optional[str] = None

    def as_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {}
        if self.locale:
            kwargs["locale"] = self.locale
        if self.pages:
            kwargs["pages"] = self.pages
        return kwargs


@dataclass
class TextLine:
    content: str
    page_number: int
    polygon: List[Any] = field(default_factory=list)


@dataclass
class LayoutBlock:
    kind: str
    content: str
    page_number: int
    polygon: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    page_number: int
    row_span: int = 1
    column_span: int = 1


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: Optional[float] = None


def normalize_text(result: Any) -> str:
    pages = getattr(result, "pages", None) or []
    lines: List[str] = []
    for page in pages:
        for line in getattr(page, "lines", None) or []:
            content = getattr(line, "content", "")
            if content:
                lines.append(content)
    if lines:
        return "\n".join(lines)
    return getattr(result, "content", "") or ""


def normalize_lines(result: Any) -> List[TextLine]:
    items: List[TextLine] = []
    for page in getattr(result, "pages", None) or []:
        page_number = getattr(page, "page_number", 1)
        for line in getattr(page, "lines", None) or []:
            items.append(
                TextLine(
                    content=getattr(line, "content", "") or "",
                    page_number=page_number,
                    polygon=list(getattr(line, "polygon", None) or []),
                )
            )
    return items


def normalize_layout(result: Any) -> List[LayoutBlock]:
    blocks: List[LayoutBlock] = []
    for page in getattr(result, "pages", None) or []:
        page_number = getattr(page, "page_number", 1)
        for line in getattr(page, "lines", None) or []:
            blocks.append(
                LayoutBlock(
                    kind="line",
                    content=getattr(line, "content", "") or "",
                    page_number=page_number,
                    polygon=list(getattr(line, "polygon", None) or []),
                )
            )
        for word in getattr(page, "words", None) or []:
            blocks.append(
                LayoutBlock(
                    kind="word",
                    content=getattr(word, "content", "") or "",
                    page_number=page_number,
                    polygon=list(getattr(word, "polygon", None) or []),
                    metadata={"confidence": getattr(word, "confidence", None)},
                )
            )
    for table_index, table in enumerate(getattr(result, "tables", None) or []):
        page_number = 1
        regions = getattr(table, "bounding_regions", None) or []
        if regions:
            page_number = getattr(regions[0], "page_number", 1)
        blocks.append(
            LayoutBlock(
                kind="table",
                content=f"table_{table_index}",
                page_number=page_number,
                polygon=list(getattr(regions[0], "polygon", None) or [])
                if regions
                else [],
                metadata={
                    "row_count": getattr(table, "row_count", 0),
                    "column_count": getattr(table, "column_count", 0),
                },
            )
        )
    return blocks


def normalize_tables(result: Any) -> List[Dict[str, Any]]:
    tables: List[Dict[str, Any]] = []
    for table in getattr(result, "tables", None) or []:
        cells: List[TableCell] = []
        row_map: Dict[int, Dict[int, str]] = {}
        for cell in getattr(table, "cells", None) or []:
            page_number = 1
            regions = getattr(cell, "bounding_regions", None) or []
            if regions:
                page_number = getattr(regions[0], "page_number", 1)
            item = TableCell(
                row_index=getattr(cell, "row_index", 0),
                column_index=getattr(cell, "column_index", 0),
                content=getattr(cell, "content", "") or "",
                page_number=page_number,
                row_span=getattr(cell, "row_span", 1) or 1,
                column_span=getattr(cell, "column_span", 1) or 1,
            )
            cells.append(item)
            row_map.setdefault(item.row_index, {})[item.column_index] = item.content
        rows = [
            [value for _, value in sorted(cols.items())]
            for _, cols in sorted(row_map.items())
        ]
        tables.append(
            {
                "row_count": getattr(table, "row_count", 0),
                "column_count": getattr(table, "column_count", 0),
                "cells": [cell.__dict__ for cell in cells],
                "rows": rows,
            }
        )
    return tables


def normalize_key_value_pairs(result: Any) -> List[Dict[str, Any]]:
    pairs: List[Dict[str, Any]] = []
    for item in getattr(result, "key_value_pairs", None) or []:
        key_obj = getattr(item, "key", None)
        value_obj = getattr(item, "value", None)
        pair = KeyValueItem(
            key=getattr(key_obj, "content", "") or "",
            value=getattr(value_obj, "content", "") or "",
            confidence=getattr(item, "confidence", None),
        )
        pairs.append(pair.__dict__)
    return pairs
