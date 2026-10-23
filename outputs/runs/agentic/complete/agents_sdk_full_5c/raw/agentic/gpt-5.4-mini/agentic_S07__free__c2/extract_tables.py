from __future__ import annotations

from typing import Any, Dict, List

from document_client import build_document_analysis_client
from document_models import TableResponse

AZURE_TABLE_MODEL = "prebuilt-layout"


def extract_tables(document_bytes: bytes) -> TableResponse:
    client = build_document_analysis_client()
    poller = client.begin_analyze_document(AZURE_TABLE_MODEL, document=document_bytes)
    result = poller.result()

    extracted: List[Dict[str, Any]] = []
    for table in getattr(result, "tables", []) or []:
        cells = []
        for cell in getattr(table, "cells", []) or []:
            cells.append({
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "content": cell.content,
                "kind": getattr(cell, "kind", None),
            })
        extracted.append({
            "row_count": table.row_count,
            "column_count": table.column_count,
            "cells": cells,
        })
    return TableResponse(tables=extracted, raw=getattr(result, "to_dict", lambda: None)())
