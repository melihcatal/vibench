from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
import os
from typing import List, Dict
from document_models import TableResponse, TableCell


def extract_tables(image_path: str, mime_type: str = "image/jpeg") -> TableResponse:
    """
    Extracts tables and their cell structures from a document using Azure Document Intelligence.

    Args:
        image_path: Path to the document image file or URL.
        mime_type: MIME type of the document (e.g., "image/jpeg", "image/png").

    Returns:
        TableResponse: Normalized response containing extracted tables and their cells.
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
            content_type=mime_type,
        )

    result: AnalyzeResult = poller.result()

    tables = []
    for table in result.tables or []:
        cells = []
        for cell in table.cells:
            cells.append(
                TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    text=cell.content,
                    is_header=cell.kind == "columnHeader" or cell.kind == "rowHeader",
                )
            )

        tables.append(
            {"rows": table.row_count, "columns": table.column_count, "cells": cells}
        )

    return TableResponse(tables=tables, pages=len(result.pages) if result.pages else 0)
