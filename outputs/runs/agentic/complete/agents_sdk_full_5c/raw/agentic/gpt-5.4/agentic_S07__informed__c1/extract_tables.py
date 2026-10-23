from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_LAYOUT_MODEL, get_document_intelligence_client, load_document_bytes
from document_models import polygon_to_dicts


def extract_tables(document_path: str) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_LAYOUT_MODEL,
        body=load_document_bytes(document_path),
    )
    result = poller.result()

    tables: List[Dict[str, Any]] = []
    for table_index, table in enumerate(result.tables or []):
        cells: List[Dict[str, Any]] = []
        rows: Dict[int, List[Dict[str, Any]]] = {}
        for cell in table.cells or []:
            item = {
                "content": cell.content,
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span,
                "page_number": (cell.bounding_regions[0].page_number if cell.bounding_regions else None),
                "polygon": polygon_to_dicts(cell.bounding_regions[0].polygon if cell.bounding_regions else None),
                "kind": getattr(cell, "kind", None),
            }
            cells.append(item)
            rows.setdefault(cell.row_index, []).append(item)
        tables.append({
            "table_index": table_index,
            "row_count": table.row_count,
            "column_count": table.column_count,
            "cells": cells,
            "rows": [rows[index] for index in sorted(rows)],
        })

    return {
        "provider": "azure-ai-documentintelligence",
        "model_id": DEFAULT_LAYOUT_MODEL,
        "tables": tables,
    }
