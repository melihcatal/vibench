from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_azure_document_intelligence_config
from document_models import OCRRequest, TableCell, TableResponse


def extract_tables(request: OCRRequest) -> TableResponse:
    config = load_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key or ""))
    with open(request.document_path, "rb") as handle:
        poller = client.begin_analyze_document("prebuilt-layout", body=handle, content_type="application/octet-stream")
    result = poller.result()
    rows = []
    for table in getattr(result, "tables", []) or []:
        table_rows = []
        for cell in getattr(table, "cells", []) or []:
            table_rows.append(
                TableCell(
                    row_index=getattr(cell, "row_index", 0),
                    column_index=getattr(cell, "column_index", 0),
                    text=getattr(cell, "content", ""),
                )
            )
        rows.append(table_rows)
    return TableResponse(rows=rows, raw=result)
