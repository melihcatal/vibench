from __future__ import annotations

from typing import List

from document_client import get_client, normalize_source
from document_models import TableCell, TableData


def extract_tables(source: str) -> List[TableData]:
    client = get_client()
    payload = normalize_source(source)
    poller = client.begin_analyze_document(model_id="prebuilt-layout", body=payload)
    result = poller.result()
    tables: List[TableData] = []
    for table in getattr(result, "tables", []) or []:
        table_data = TableData(page_number=getattr(table, "bounding_regions", [None])[0].page_number if getattr(table, "bounding_regions", None) else None)
        for cell in getattr(table, "cells", []) or []:
            table_data.cells.append(
                TableCell(
                    row_index=getattr(cell, "row_index", 0),
                    column_index=getattr(cell, "column_index", 0),
                    text=getattr(cell, "content", ""),
                    row_span=getattr(cell, "row_span", 1),
                    column_span=getattr(cell, "column_span", 1),
                )
            )
        tables.append(table_data)
    return tables
