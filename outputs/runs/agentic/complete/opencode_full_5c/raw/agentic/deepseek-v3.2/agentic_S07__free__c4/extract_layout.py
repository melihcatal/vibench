import os
from typing import List, Dict, Any, Optional
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_client
from document_models import LayoutElement, LayoutExtractionResult


def extract_layout(image_path: str) -> LayoutExtractionResult:
    """
    Extract blocks, lines, tables, and layout elements from a document using Azure Form Recognizer.

    Args:
        image_path: Path to the image file

    Returns:
        LayoutExtractionResult containing layout elements and structure
    """
    client = get_azure_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout", document=image_data
    )

    result = poller.result()

    layout_elements = []

    for page in result.pages:
        for line in page.lines:
            layout_elements.append(
                LayoutElement(
                    type="line",
                    text=line.content,
                    bounding_box=line.polygon,
                    page_number=page.page_number,
                    confidence=line.confidence if hasattr(line, "confidence") else 1.0,
                )
            )

    for table in result.tables:
        for cell in table.cells:
            layout_elements.append(
                LayoutElement(
                    type="table_cell",
                    text=cell.content,
                    bounding_box=cell.polygon,
                    page_number=cell.page_number,
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    confidence=cell.confidence if hasattr(cell, "confidence") else 1.0,
                )
            )

    return LayoutExtractionResult(
        elements=layout_elements,
        provider="azure_form_recognizer",
        model_id="prebuilt-layout",
        page_count=len(result.pages),
    )
