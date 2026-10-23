from typing import Dict, List, Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeDocumentRequest,
    AnalyzeResult,
    DocumentTable,
)
from azure.core.credentials import AzureKeyCredential


def extract_tables(image_path: str) -> List[Dict]:
    """
    Extracts table cells and row structure from a document using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
        )

    result: AnalyzeResult = poller.result()

    tables = []

    if result.tables:
        for table in result.tables:
            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": [],
            }
            for cell in table.cells:
                cell_data = {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "content": cell.content,
                    "is_header": cell.kind == "columnHeader"
                    or cell.kind == "rowHeader",
                }
                table_data["cells"].append(cell_data)
            tables.append(table_data)

    return tables
