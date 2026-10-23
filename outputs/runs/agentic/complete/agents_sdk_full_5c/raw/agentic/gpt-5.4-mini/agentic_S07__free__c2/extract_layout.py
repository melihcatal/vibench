from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import build_document_analysis_client
from document_models import LayoutResponse

AZURE_LAYOUT_MODEL = "prebuilt-layout"


def extract_layout(document_bytes: bytes) -> LayoutResponse:
    client = build_document_analysis_client()
    poller = client.begin_analyze_document(AZURE_LAYOUT_MODEL, document=document_bytes)
    result = poller.result()

    blocks: List[Dict[str, Any]] = []
    lines: List[Dict[str, Any]] = []
    tables: List[Dict[str, Any]] = []

    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            lines.append({"content": line.content, "page_number": page.page_number})
    for paragraph in getattr(result, "paragraphs", []) or []:
        blocks.append({"content": paragraph.content, "role": getattr(paragraph, "role", None)})
    for table in getattr(result, "tables", []) or []:
        tables.append({"row_count": table.row_count, "column_count": table.column_count, "cells": [cell.to_dict() for cell in table.cells]})

    return LayoutResponse(blocks=blocks, lines=lines, tables=tables, raw=getattr(result, "to_dict", lambda: None)())
