from __future__ import annotations

from typing import List, Optional

from document_client import DocumentServiceClient
from document_models import DocumentRequest, TableCell, TableResponse


def extract_tables(document_path: Optional[str] = None, document_bytes: Optional[bytes] = None) -> TableResponse:
    request = DocumentRequest(document_path=document_path, document_bytes=document_bytes)
    client = DocumentServiceClient()
    result = client.analyze(request, model_id="prebuilt-layout")
    cells: List[TableCell] = []
    for table in getattr(result, "tables", []) or []:
        for cell in getattr(table, "cells", []) or []:
            cells.append(
                TableCell(
                    row_index=getattr(cell, "row_index", 0),
                    column_index=getattr(cell, "column_index", 0),
                    text=getattr(cell, "content", ""),
                    row_span=getattr(cell, "row_span", 1),
                    column_span=getattr(cell, "column_span", 1),
                    metadata={"kind": getattr(cell, "kind", None)},
                )
            )
    return TableResponse(cells=cells, provider="azure-document-intelligence", metadata={"model_id": "prebuilt-layout"})
