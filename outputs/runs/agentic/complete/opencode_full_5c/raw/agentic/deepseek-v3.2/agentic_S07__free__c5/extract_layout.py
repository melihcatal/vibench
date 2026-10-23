import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_form_recognizer_client
from document_models import (
    LayoutExtractionRequest,
    LayoutExtractionResponse,
    LayoutBlock,
)


def extract_layout(request: LayoutExtractionRequest) -> LayoutExtractionResponse:
    """Extract blocks, lines, tables, or layout elements from a document using Azure Form Recognizer."""
    client = get_form_recognizer_client()

    with open(request.document_path, "rb") as document:
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout", document=document
        )

    result = poller.result()

    blocks = []

    for page in result.pages:
        for line in page.lines:
            blocks.append(
                LayoutBlock(
                    text=line.content,
                    bounding_box=line.bounding_box,
                    type="line",
                    confidence=line.confidence if hasattr(line, "confidence") else 0.9,
                )
            )

    for table in result.tables:
        blocks.append(
            LayoutBlock(
                text=f"Table with {table.row_count} rows and {table.column_count} columns",
                bounding_box=table.bounding_box,
                type="table",
                confidence=0.9,
            )
        )

    return LayoutExtractionResponse(
        blocks=blocks,
        provider="azure-form-recognizer",
        model_id="prebuilt-layout",
        raw_response=result,
    )
