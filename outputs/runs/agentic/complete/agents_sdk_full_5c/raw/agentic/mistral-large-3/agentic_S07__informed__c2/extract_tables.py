from typing import List, Dict, Any
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_intelligence_client
from document_models import TableExtractionResponse


def extract_tables_from_image(image_path: str, mime_type: str = "image/jpeg") -> TableExtractionResponse:
    """Extract table cells and row structure from a document using Azure Document Intelligence."""
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type
        )
    
    result: AnalyzeResult = poller.result()
    
    tables = []
    for table in result.tables:
        cells = []
        for cell in table.cells:
            cells.append({
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "text": cell.content,
                "is_header": cell.kind == "columnHeader" or cell.kind == "rowHeader",
                "bounding_box": cell.polygon,
                "confidence": cell.confidence
            })
        tables.append({
            "row_count": table.row_count,
            "column_count": table.column_count,
            "cells": cells
        })
    
    return TableExtractionResponse(tables=tables)