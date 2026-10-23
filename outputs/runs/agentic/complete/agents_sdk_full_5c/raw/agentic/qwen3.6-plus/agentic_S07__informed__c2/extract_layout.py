"""
Extracts blocks, lines, tables, and layout elements from a document
using Azure AI Document Intelligence prebuilt-layout model.
"""

import os
from typing import List

from document_client import (
    create_document_client,
    read_image_bytes,
    normalize_azure_poller_response,
)
from document_models import (
    DocumentLayoutResult,
    LayoutElement,
    TableData,
    normalize_layout_result,
)

# Azure Document Intelligence prebuilt-layout model identifier
AZURE_LAYOUT_MODEL_ID = "prebuilt-layout"


def extract_layout_from_image(
    file_path: str,
    model_id: str = AZURE_LAYOUT_MODEL_ID,
) -> DocumentLayoutResult:
    """
    Extract layout elements (paragraphs, headings, tables, figures) from a document
    using Azure AI Document Intelligence.

    Args:
        file_path: Path to the document image or PDF file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-layout'.

    Returns:
        DocumentLayoutResult: Normalized result containing layout elements and tables.

    Raises:
        ValueError: If required Azure environment variables are not set.
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")

    file_bytes = read_image_bytes(file_path)
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": file_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    normalized = normalize_layout_result(result)
    return normalized


def extract_layout_from_bytes(
    file_bytes: bytes,
    model_id: str = AZURE_LAYOUT_MODEL_ID,
) -> DocumentLayoutResult:
    """
    Extract layout elements from document bytes using Azure AI Document Intelligence.

    Args:
        file_bytes: Raw bytes of the document file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-layout'.

    Returns:
        DocumentLayoutResult: Normalized result containing layout elements and tables.
    """
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": file_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    normalized = normalize_layout_result(result)
    return normalized


def get_layout_elements_by_type(
    layout_result: DocumentLayoutResult,
    element_type: str,
) -> List[LayoutElement]:
    """
    Filter layout elements by their type.

    Args:
        layout_result: The full layout extraction result.
        element_type: Type to filter by (e.g., 'paragraph', 'sectionHeading', 'table').

    Returns:
        List[LayoutElement]: Filtered list of layout elements.
    """
    return [
        elem for elem in layout_result.elements
        if elem.element_type == element_type
    ]


def extract_tables_from_layout(
    layout_result: DocumentLayoutResult,
) -> List[TableData]:
    """
    Extract table data from a layout result.

    Args:
        layout_result: The full layout extraction result.

    Returns:
        List[TableData]: List of extracted tables.
    """
    return layout_result.tables
