import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_config


def extract_tables(document_bytes: bytes):
    cfg = require_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document(
        "prebuilt-layout", body=io.BytesIO(document_bytes)
    )
    result = poller.result()
    tables = []
    for table in getattr(result, "tables", []):
        tables.append(
            {
                "row_count": getattr(table, "row_count", 0),
                "column_count": getattr(table, "column_count", 0),
                "cells": [
                    getattr(cell, "content", "") for cell in getattr(table, "cells", [])
                ],
            }
        )
    return tables
