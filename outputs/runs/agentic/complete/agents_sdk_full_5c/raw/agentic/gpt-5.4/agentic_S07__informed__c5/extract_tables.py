from __future__ import annotations

from document_client import DEFAULT_MODEL_LAYOUT, OCRClientFactory, load_bytes
from document_models import TableExtractionResult, to_bounding_regions


def extract_tables(document_path: str) -> TableExtractionResult:
    client = OCRClientFactory().create_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_MODEL_LAYOUT,
        body=load_bytes(document_path),
        content_type="application/octet-stream",
    )
    result = poller.result()
    tables = []
    for table in result.tables or []:
        cells = []
        rows = {}
        for cell in table.cells or []:
            cell_payload = {
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span,
                "kind": getattr(cell, "kind", None),
                "content": cell.content or "",
                "bounding_regions": [r.__dict__ for r in to_bounding_regions(getattr(cell, "bounding_regions", None))],
            }
            cells.append(cell_payload)
            rows.setdefault(cell.row_index, []).append(cell_payload)
        tables.append(
            {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": cells,
                "rows": [rows[idx] for idx in sorted(rows)],
            }
        )
    return TableExtractionResult(tables=tables, model_id=DEFAULT_MODEL_LAYOUT)
