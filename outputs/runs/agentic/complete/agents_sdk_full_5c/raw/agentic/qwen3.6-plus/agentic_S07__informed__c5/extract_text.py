"""
extract_text.py - Extract plain text from a scanned document image
using Azure AI Document Intelligence OCR.

Provider: Azure AI Document Intelligence
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

from document_client import get_document_client, read_document_bytes, get_analysis_features
from document_models import OcrResponse, normalize_azure_text_result


def extract_text(file_path: str) -> OcrResponse:
    """
    Extract plain text from a scanned document image or PDF using
    Azure Document Intelligence with the OCR model.

    Args:
        file_path: Path to the document file (image or PDF).

    Returns:
        OcrResponse containing extracted text and text blocks.
    """
    client = get_document_client()
    document_bytes = read_document_bytes(file_path)

    features = get_analysis_features(mode="ocr")

    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_text_result(result)


def extract_text_from_bytes(document_bytes: bytes) -> OcrResponse:
    """
    Extract plain text from document bytes using Azure Document Intelligence OCR.

    Args:
        document_bytes: Raw bytes of the document.

    Returns:
        OcrResponse containing extracted text and text blocks.
    """
    client = get_document_client()
    features = get_analysis_features(mode="ocr")

    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=document_bytes,
        features=features,
    )
    result = poller.result()

    return normalize_azure_text_result(result)
