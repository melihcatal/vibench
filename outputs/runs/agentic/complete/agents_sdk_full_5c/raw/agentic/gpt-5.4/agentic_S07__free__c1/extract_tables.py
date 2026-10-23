from __future__ import annotations

from document_client import ensure_bytes, get_document_intelligence_client
from document_models import TableResult, polygon_to_bbox


def extract_tables(document_bytes: bytes, model_id: str = "prebuilt-layout") -> TableResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(model_id=model_id, body=ensure_bytes(document_bytes))
    result = poller.result().as_dict()

    tables = []
    for table in result.get("tables", []):
        cells = []
        for cell in table.get("cells", []):
            cells.append(
                {
                    "row_index": cell.get("rowIndex", 0),
                    "column_index": cell.get("columnIndex", 0),
                    "text": cell.get("content", ""),
                    "row_span": cell.get("rowSpan", 1),
                    "column_span": cell.get("columnSpan", 1),
                    "is_header": cell.get("kind") in {"columnHeader", "rowHeader", "stubHead"},
                    "bbox": polygon_to_bbox(cell.get("boundingRegions", [{}])[0].get("polygon")) if cell.get("boundingRegions") else None,
                }
            )
        tables.append(
            {
                "provider": "Azure Document Intelligence",
                "row_count": table.get("rowCount", 0),
                "column_count": table.get("columnCount", 0),
                "cells": cells,
            }
        )

    return TableResult(provider="azure-document-intelligence", tables=tables, raw=result)
