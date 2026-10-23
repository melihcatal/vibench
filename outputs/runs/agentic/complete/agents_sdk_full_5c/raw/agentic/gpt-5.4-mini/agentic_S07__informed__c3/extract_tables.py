from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, request_to_stream
from document_models import DocumentRequest, DocumentTableCell, DocumentTableResult


def extract_tables(request: DocumentRequest) -> DocumentTableResult:
    client = build_client()
    source = request_to_stream(request)
    if isinstance(source, str):
        poller = client.begin_analyze_document("prebuilt-layout", AnalyzeDocumentRequest(url_source=source))
    else:
        poller = client.begin_analyze_document("prebuilt-layout", body=source)
    result = poller.result()
    cells = []
    row_count = 0
    column_count = 0
    for table in getattr(result, "tables", []) or []:
        for cell in getattr(table, "cells", []) or []:
            cells.append(DocumentTableCell(row_index=getattr(cell, "row_index", 0), column_index=getattr(cell, "column_index", 0), text=getattr(cell, "content", ""), confidence=getattr(cell, "confidence", None), row_span=getattr(cell, "row_span", 1), column_span=getattr(cell, "column_span", 1), raw=cell))
            row_count = max(row_count, getattr(cell, "row_index", 0) + getattr(cell, "row_span", 1))
            column_count = max(column_count, getattr(cell, "column_index", 0) + getattr(cell, "column_span", 1))
    return DocumentTableResult(cells=cells, row_count=row_count or None, column_count=column_count or None, provider="azure-ai-documentintelligence", raw=result)
