from azure.ai.documentintelligence import AnalyzeDocumentRequest

from document_client import create_client
from document_models import TableResult


def extract_tables(content_bytes: bytes, mime_type: str = "image/png") -> TableResult:
    client = create_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=AnalyzeDocumentRequest(bytes_source=content_bytes),
        content_type=mime_type,
    )
    result = poller.result()
    rows = []
    for table in getattr(result, "tables", []) or []:
        table_rows = {}
        for cell in getattr(table, "cells", []) or []:
            row = getattr(cell, "row_index", 0)
            col = getattr(cell, "column_index", 0)
            table_rows.setdefault(row, {})[col] = getattr(cell, "content", "")
        for row_index in sorted(table_rows):
            rows.append(
                [table_rows[row_index][col] for col in sorted(table_rows[row_index])]
            )
    return TableResult(rows=rows, raw={"result": result})
