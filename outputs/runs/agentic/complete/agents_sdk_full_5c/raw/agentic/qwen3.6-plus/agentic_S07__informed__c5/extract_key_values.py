"""
extract_key_values.py - Extract key-value pairs from a form-like document
using Azure AI Document Intelligence general document model.

Provider: Azure AI Document Intelligence
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

from document_client import get_document_client, read_document_bytes, get_analysis_features
from document_models import KeyValueResponse, normalize_azure_keyvalue_result


def extract_key_values(file_path: str) -> KeyValueResponse:
    """
    Extract key-value pairs from a form-like document using
    Azure Document Intelligence general document model (prebuilt-document).

    Args:
        file_path: Path to the document file (image or PDF).

    Returns:
        KeyValueResponse containing extracted key-value pairs.
    """
    client = get_document_client()
    document_bytes = read_document_bytes(file_path)

    features = get_analysis_features(mode="key_value")

    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_keyvalue_result(result)


def extract_key_values_from_bytes(document_bytes: bytes) -> KeyValueResponse:
    """
    Extract key-value pairs from document bytes.

    Args:
        document_bytes: Raw bytes of the document.

    Returns:
        KeyValueResponse containing extracted key-value pairs.
    """
    client = get_document_client()
    features = get_analysis_features(mode="key_value")

    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_keyvalue_result(result)
