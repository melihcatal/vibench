from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_endpoint, load_config, require_bytes
from document_models import TableResult


def extract_tables(document: bytes, mime_type: str = "image/png") -> TableResult:
    config = load_config()
    client = DocumentIntelligenceClient(
        ensure_endpoint(config), AzureKeyCredential(config.api_key or "")
    )
    poller = client.begin_analyze_document(
        "prebuilt-layout", require_bytes(document), content_type=mime_type
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
                    "content": getattr(cell, "content", ""),
                }
            )
        tables.append(
            {
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
                "cells": cells,
            }
        )
    return TableResult(
        tables=tables, raw=result.as_dict() if hasattr(result, "as_dict") else None
    )
