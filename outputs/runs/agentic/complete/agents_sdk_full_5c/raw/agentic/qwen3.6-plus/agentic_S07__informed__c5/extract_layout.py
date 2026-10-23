"""
extract_layout.py - Extract blocks, lines, tables, or layout elements from a document
using Azure AI Document Intelligence Layout model.

Provider: Azure AI Document Intelligence
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

from document_client import get_document_client, read_document_bytes, get_analysis_features
from document_models import LayoutResponse, normalize_azure_layout_result


def extract_layout(file_path: str) -> LayoutResponse:
    """
    Extract layout elements (paragraphs, headings, tables, figures, etc.)
    from a document using Azure Document Intelligence Layout model.

    Args:
        file_path: Path to the document file (image or PDF).

    Returns:
        LayoutResponse containing layout blocks, tables, and page count.
    """
    client = get_document_client()
    document_bytes = read_document_bytes(file_path)

    features = get_analysis_features(mode="layout")

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_layout_result(result)


def extract_layout_from_bytes(document_bytes: bytes) -> LayoutResponse:
    """
    Extract layout elements from document bytes using Azure Document Intelligence.

    Args:
        document_bytes: Raw bytes of the document.

    Returns:
        LayoutResponse containing layout blocks, tables, and page count.
    """
    client = get_document_client()
    features = get_analysis_features(mode="layout")

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_layout_result(result)
