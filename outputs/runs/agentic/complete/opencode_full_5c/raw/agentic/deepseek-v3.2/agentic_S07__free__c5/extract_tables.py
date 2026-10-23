import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_form_recognizer_client
from document_models import (
    TableExtractionRequest,
    TableExtractionResponse,
    Table,
    TableCell,
)


def extract_tables(request: TableExtractionRequest) -> TableExtractionResponse:
    """Extract table cells and row structure from a document using Azure Form Recognizer."""
    client = get_form_recognizer_client()

    with open(request.document_path, "rb") as document:
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout", document=document
        )

    result = poller.result()

    tables = []

    for table_idx, table in enumerate(result.tables):
        cells = []
        for cell in table.cells:
            cells.append(
                TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    content=cell.content,
                    bounding_box=cell.bounding_box,
                    confidence=cell.confidence if hasattr(cell, "confidence") else 0.9,
                )
            )

        tables.append(
            Table(
                table_index=table_idx,
                row_count=table.row_count,
                column_count=table.column_count,
                cells=cells,
                bounding_box=table.bounding_box,
            )
        )

    return TableExtractionResponse(
        tables=tables,
        provider="azure-form-recognizer",
        model_id="prebuilt-layout",
        raw_response=result,
    )
