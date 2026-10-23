from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_service_config


def extract_tables(document_url: str):
    cfg = load_document_service_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document("prebuilt-layout", document_url)
    result = poller.result()
    tables = []
    for table in result.tables:
        cells = []
        for cell in table.cells:
            cells.append(
                {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "content": cell.content,
                }
            )
        tables.append(
            {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": cells,
            }
        )
    return tables
