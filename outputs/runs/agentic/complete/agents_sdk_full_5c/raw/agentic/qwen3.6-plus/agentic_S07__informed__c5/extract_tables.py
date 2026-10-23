"""
extract_tables.py - Extract table cells and row structure from a document
using Azure AI Document Intelligence Layout model.

Provider: Azure AI Document Intelligence
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

from document_client import get_document_client, read_document_bytes, get_analysis_features
from document_models import TableResponse, normalize_azure_table_result


def extract_tables(file_path: str) -> TableResponse:
    """
    Extract table cells and row structure from a document using
    Azure Document Intelligence Layout model.

    Args:
        file_path: Path to the document file (image or PDF).

    Returns:
        TableResponse containing extracted tables with rows and cells.
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

    return normalize_azure_table_result(result)


def extract_tables_from_bytes(document_bytes: bytes) -> TableResponse:
    """
    Extract table cells and row structure from document bytes.

    Args:
        document_bytes: Raw bytes of the document.

    Returns:
        TableResponse containing extracted tables with rows and cells.
    """
    client = get_document_client()
    features = get_analysis_features(mode="layout")

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_table_result(result)
