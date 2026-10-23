from document_client import get_document_intelligence_client, get_prebuilt_model_id
from document_models import TableExtractionResult


def extract_tables(file_path: str) -> TableExtractionResult:
    client = get_document_intelligence_client()
    with open(file_path, "rb") as stream:
        poller = client.begin_analyze_document(
            get_prebuilt_model_id("tables"), body=stream
        )
    result = poller.result()
    tables = []
    for table in getattr(result, "tables", []) or []:
        cells = []
        for cell in getattr(table, "cells", []) or []:
            cells.append(
                {
                    "row_index": getattr(cell, "row_index", None),
                    "column_index": getattr(cell, "column_index", None),
                    "content": getattr(cell, "content", None),
                }
            )
        tables.append(
            {
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
                "cells": cells,
            }
        )
    return TableExtractionResult(tables=tables)
