from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import (
    get_azure_document_intelligence_endpoint,
    get_azure_document_intelligence_key,
    open_document_bytes,
)
from document_models import DocumentInput, TableResponse


def extract_tables(document: DocumentInput) -> TableResponse:
    client = DocumentIntelligenceClient(
        endpoint=get_azure_document_intelligence_endpoint(),
        credential=AzureKeyCredential(get_azure_document_intelligence_key()),
    )
    poller = client.begin_analyze_document(
        "prebuilt-layout", open_document_bytes(document.source)
    )
    result = poller.result()
    tables = []
    for table in getattr(result, "tables", []) or []:
        tables.append(
            {
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
                "cells": [
                    getattr(cell, "content", "")
                    for cell in getattr(table, "cells", []) or []
                ],
            }
        )
    return TableResponse(tables=tables, raw={"model_id": "prebuilt-layout"})
