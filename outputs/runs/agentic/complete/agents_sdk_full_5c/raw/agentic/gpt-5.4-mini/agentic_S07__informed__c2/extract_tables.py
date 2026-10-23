from __future__ import annotations

from document_client import analyze_document, get_client
from document_models import DocumentInput, TableCell, normalize_table_cells

PROVIDER = "Azure AI Document Intelligence"
MODEL_ID = "prebuilt-layout"


def extract_tables(document_bytes: bytes, mime_type: str = "image/png") -> list[list[TableCell]]:
    client = get_client()
    document = DocumentInput(content=document_bytes, mime_type=mime_type)
    result = analyze_document(client, document, model_id=MODEL_ID)
    tables: list[list[TableCell]] = []
    for table in getattr(result, "tables", []):
        raw_cells = []
        for cell in getattr(table, "cells", []):
            raw_cells.append(
                {
                    "row_index": getattr(cell, "row_index", 0),
                    "column_index": getattr(cell, "column_index", 0),
                    "text": getattr(cell, "content", ""),
                    "row_span": getattr(cell, "row_span", 1),
                    "column_span": getattr(cell, "column_span", 1),
                }
            )
        tables.append(normalize_table_cells(raw_cells))
    return tables
