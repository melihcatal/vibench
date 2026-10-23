from __future__ import annotations

from typing import List

from document_client import begin_analyze_document
from document_models import TableCell, TableResponse


def extract_tables(document) -> List[TableResponse]:
    poller = begin_analyze_document("prebuilt-layout", document, content_type="application/octet-stream")
    result = poller.result()
    tables: List[TableResponse] = []

    for table in getattr(result, "tables", []) or []:
        cells: List[TableCell] = []
        max_row = 0
        max_col = 0
        for cell in getattr(table, "cells", []) or []:
            row_index = int(getattr(cell, "row_index", 0) or 0)
            col_index = int(getattr(cell, "column_index", 0) or 0)
            max_row = max(max_row, row_index)
            max_col = max(max_col, col_index)
            cells.append(
                TableCell(
                    row_index=row_index,
                    column_index=col_index,
                    content=getattr(cell, "content", "") or "",
                    row_span=int(getattr(cell, "row_span", 1) or 1),
                    column_span=int(getattr(cell, "column_span", 1) or 1),
                )
            )
        rows = [["" for _ in range(max_col + 1)] for _ in range(max_row + 1)] if cells else []
        for cell in cells:
            if rows:
                rows[cell.row_index][cell.column_index] = cell.content
        tables.append(TableResponse(rows=rows, cells=cells))

    return tables
