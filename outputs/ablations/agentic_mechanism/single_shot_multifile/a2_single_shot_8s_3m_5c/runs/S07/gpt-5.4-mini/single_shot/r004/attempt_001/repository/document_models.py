from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class DocumentImageRequest:
    path: str
    data: bytes

    @classmethod
    def from_path(cls, path: str) -> "DocumentImageRequest":
        return cls(path=path, data=Path(path).read_bytes())


def _page_text(page: Any) -> str:
    lines = []
    for line in getattr(page, "lines", []) or []:
        content = getattr(line, "content", None)
        if content:
            lines.append(content)
    return "\n".join(lines)


def first_result_from_analyze(result: Any) -> str:
    pages = getattr(result, "pages", []) or []
    texts = [_page_text(page) for page in pages]
    return "\n".join([t for t in texts if t]).strip()


def extract_layout_elements(result: Any) -> list[dict]:
    elements: list[dict] = []
    pages = getattr(result, "pages", []) or []
    for page_index, page in enumerate(pages):
        for line in getattr(page, "lines", []) or []:
            elements.append({"type": "line", "page": page_index + 1, "content": getattr(line, "content", ""), "polygon": getattr(line, "polygon", None)})
    for table_index, table in enumerate(getattr(result, "tables", []) or []):
        elements.append({"type": "table", "table_index": table_index, "row_count": len(getattr(table, "rows", []) or []), "column_count": len(getattr(table, "cells", []) or [])})
    return elements


def extract_tables(result: Any) -> list[dict]:
    tables_out: list[dict] = []
    for table_index, table in enumerate(getattr(result, "tables", []) or []):
        cells_out: list[dict] = []
        for cell in getattr(table, "cells", []) or []:
            cells_out.append({"row_index": getattr(cell, "row_index", None), "column_index": getattr(cell, "column_index", None), "content": getattr(cell, "content", None), "kind": getattr(cell, "kind", None), "row_span": getattr(cell, "row_span", None), "column_span": getattr(cell, "column_span", None)})
        tables_out.append({"table_index": table_index, "cells": cells_out})
    return tables_out


def extract_key_values(result: Any) -> list[dict]:
    pairs: list[dict] = []
    for item in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(item, "key", None), "content", None)
        value = getattr(getattr(item, "value", None), "content", None)
        pairs.append({"key": key, "value": value})
    return pairs


def normalize_text_response(text: str, raw: Any) -> dict:
    return {"text": text, "raw": raw}


def normalize_layout_response(elements: list[dict], raw: Any) -> dict:
    return {"elements": elements, "raw": raw}


def normalize_tables_response(tables: list[dict], raw: Any) -> dict:
    return {"tables": tables, "raw": raw}


def normalize_kv_response(items: list[dict], raw: Any) -> dict:
    return {"key_values": items, "raw": raw}
