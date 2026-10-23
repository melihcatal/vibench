from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_config
from document_models import DocumentRequest, DocumentResponse, normalize_text


def extract_tables(request: DocumentRequest) -> DocumentResponse:
    cfg = get_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(cfg["endpoint"], AzureKeyCredential(cfg["key"]))
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        analyze_request=request.content,
        content_type=request.mime_type,
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
                    "content": normalize_text(getattr(cell, "content", "")),
                }
            )
        tables.append(
            {
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
                "cells": cells,
            }
        )
    return DocumentResponse(
        tables=tables, text=normalize_text(getattr(result, "content", "")), raw=result
    )
