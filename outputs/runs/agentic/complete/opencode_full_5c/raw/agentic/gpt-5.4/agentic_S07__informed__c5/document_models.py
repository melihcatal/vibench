from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    file_path: str
    mime_type: str = "application/octet-stream"
    model_id: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class OCRLine:
    text: str
    page: int
    polygon: List[float] = field(default_factory=list)
    confidence: Optional[float] = None


@dataclass
class LayoutElement:
    kind: str
    text: str
    page: int
    polygon: List[float] = field(default_factory=list)
    row_count: Optional[int] = None
    column_count: Optional[int] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    page: int
    row_span: int = 1
    column_span: int = 1


@dataclass
class KeyValueItem:
    key: str
    value: str
    page: int
    confidence: Optional[float] = None


def _polygon_to_list(polygon: Any) -> List[float]:
    if polygon is None:
        return []
    values: List[float] = []
    for point in polygon:
        if hasattr(point, "x") and hasattr(point, "y"):
            values.extend([float(point.x), float(point.y)])
        elif isinstance(point, (list, tuple)) and len(point) >= 2:
            values.extend([float(point[0]), float(point[1])])
    return values


def normalize_ocr_lines(result: Any) -> List[OCRLine]:
    lines: List[OCRLine] = []
    for page_index, page in enumerate(getattr(result, "pages", []) or [], start=1):
        for line in getattr(page, "lines", []) or []:
            lines.append(
                OCRLine(
                    text=(getattr(line, "content", None) or "").strip(),
                    page=page_index,
                    polygon=_polygon_to_list(getattr(line, "polygon", None)),
                    confidence=getattr(line, "confidence", None),
                )
            )
    return lines


def normalize_layout_elements(result: Any) -> List[LayoutElement]:
    elements: List[LayoutElement] = []
    for page_index, page in enumerate(getattr(result, "pages", []) or [], start=1):
        for line in getattr(page, "lines", []) or []:
            elements.append(
                LayoutElement(
                    kind="line",
                    text=(getattr(line, "content", None) or "").strip(),
                    page=page_index,
                    polygon=_polygon_to_list(getattr(line, "polygon", None)),
                )
            )
    for table in getattr(result, "tables", []) or []:
        elements.append(
            LayoutElement(
                kind="table",
                text=" ".join(
                    (getattr(cell, "content", None) or "").strip()
                    for cell in getattr(table, "cells", []) or []
                ).strip(),
                page=(
                    getattr(table, "bounding_regions", [None])[0].page_number
                    if getattr(table, "bounding_regions", None)
                    else 1
                ),
                polygon=_polygon_to_list(
                    (
                        getattr(table, "bounding_regions", [None])[0].polygon
                        if getattr(table, "bounding_regions", None)
                        else None
                    )
                ),
                row_count=getattr(table, "row_count", None),
                column_count=getattr(table, "column_count", None),
            )
        )
    for kv in getattr(result, "key_value_pairs", []) or []:
        key_text = getattr(getattr(kv, "key", None), "content", None) or ""
        value_text = getattr(getattr(kv, "value", None), "content", None) or ""
        page_number = 1
        if getattr(kv, "key", None) and getattr(kv.key, "bounding_regions", None):
            page_number = kv.key.bounding_regions[0].page_number
        elements.append(
            LayoutElement(
                kind="key_value",
                text=f"{key_text}: {value_text}".strip(),
                page=page_number,
                polygon=_polygon_to_list(
                    (
                        kv.key.bounding_regions[0].polygon
                        if getattr(kv, "key", None)
                        and getattr(kv.key, "bounding_regions", None)
                        else None
                    )
                ),
            )
        )
    return elements


def normalize_table_cells(result: Any) -> List[TableCell]:
    cells: List[TableCell] = []
    for table in getattr(result, "tables", []) or []:
        page_number = (
            getattr(table, "bounding_regions", [None])[0].page_number
            if getattr(table, "bounding_regions", None)
            else 1
        )
        for cell in getattr(table, "cells", []) or []:
            cells.append(
                TableCell(
                    row_index=int(getattr(cell, "row_index", 0)),
                    column_index=int(getattr(cell, "column_index", 0)),
                    text=(getattr(cell, "content", None) or "").strip(),
                    page=page_number,
                    row_span=int(getattr(cell, "row_span", 1) or 1),
                    column_span=int(getattr(cell, "column_span", 1) or 1),
                )
            )
    return cells


def normalize_key_value_pairs(result: Any) -> List[KeyValueItem]:
    items: List[KeyValueItem] = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key_text = (getattr(getattr(kv, "key", None), "content", None) or "").strip()
        value_text = (
            getattr(getattr(kv, "value", None), "content", None) or ""
        ).strip()
        if not key_text:
            continue
        page_number = 1
        if getattr(kv, "key", None) and getattr(kv.key, "bounding_regions", None):
            page_number = kv.key.bounding_regions[0].page_number
        items.append(
            KeyValueItem(
                key=key_text,
                value=value_text,
                page=page_number,
                confidence=getattr(kv, "confidence", None),
            )
        )
    return items


def lines_to_text(lines: List[OCRLine]) -> str:
    return "\n".join(line.text for line in lines if line.text)


def as_dict_list(items: List[Any]) -> List[Dict[str, Any]]:
    return [item.__dict__.copy() for item in items]
