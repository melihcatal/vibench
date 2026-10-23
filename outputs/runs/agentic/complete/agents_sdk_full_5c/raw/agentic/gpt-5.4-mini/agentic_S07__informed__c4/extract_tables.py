from __future__ import annotations

from typing import List

from document_client import DocumentAIClientHelper
from document_models import DocumentRequest, TableCell, TableResult, normalize_text


def extract_tables(file_path: str, mime_type: str = "image/png") -> List[TableResult]:
    helper = DocumentAIClientHelper()
    response = helper.process(DocumentRequest(file_path=file_path, mime_type=mime_type))
    document = response.document
    tables: List[TableResult] = []
    for page in getattr(document, "pages", []):
        for table in getattr(page, "tables", []):
            cells: List[TableCell] = []
            rows: List[List[str]] = []
            for row_index, row in enumerate(getattr(table, "body_rows", [])):
                row_values: List[str] = []
                for column_index, cell in enumerate(getattr(row, "cells", [])):
                    text = normalize_text(getattr(cell, "layout", {}).get("text_anchor", {}))
                    cells.append(TableCell(row_index=row_index, column_index=column_index, text=text, raw=cell))
                    row_values.append(text)
                rows.append(row_values)
            tables.append(TableResult(cells=cells, rows=rows, raw=table))
    return tables
