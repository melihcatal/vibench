import os
from typing import List, Dict, Any, Optional
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_client
from document_models import Table, TableCell, TableExtractionResult


def extract_tables(image_path: str) -> TableExtractionResult:
    """
    Extract table cells and row structure from a document using Azure Form Recognizer.

    Args:
        image_path: Path to the image file

    Returns:
        TableExtractionResult containing extracted tables
    """
    client = get_azure_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout", document=image_data
    )

    result = poller.result()

    tables = []

    for table in result.tables:
        cells = []
        for cell in table.cells:
            cells.append(
                TableCell(
                    content=cell.content,
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    row_span=cell.row_span,
                    column_span=cell.column_span,
                    bounding_box=cell.polygon,
                    confidence=cell.confidence if hasattr(cell, "confidence") else 1.0,
                )
            )

        tables.append(
            Table(
                cells=cells,
                row_count=table.row_count,
                column_count=table.column_count,
                page_number=table.page_number,
            )
        )

    return TableExtractionResult(
        tables=tables,
        provider="azure_form_recognizer",
        model_id="prebuilt-layout",
        total_tables=len(tables),
    )
