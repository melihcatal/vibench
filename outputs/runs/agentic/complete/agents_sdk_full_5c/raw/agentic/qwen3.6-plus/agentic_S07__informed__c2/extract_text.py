"""
Extracts plain text from a scanned document image using Azure AI Document Intelligence.
Uses the 'prebuilt-read' model for OCR text extraction.
"""

import os
from typing import Optional

from azure.ai.documentintelligence.models import AnalyzeResult

from document_client import (
    create_document_client,
    read_image_bytes,
    normalize_azure_poller_response,
)
from document_models import (
    DocumentTextResult,
    normalize_ocr_text_result,
)

# Azure Document Intelligence prebuilt-read model identifier for OCR
AZURE_OCR_MODEL_ID = "prebuilt-read"


def extract_text_from_image(
    file_path: str,
    model_id: str = AZURE_OCR_MODEL_ID,
) -> DocumentTextResult:
    """
    Extract plain text from a scanned document image using Azure AI Document Intelligence.

    Args:
        file_path: Path to the document image file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-read'.

    Returns:
        DocumentTextResult: Normalized OCR result containing full text and text blocks.

    Raises:
        ValueError: If required Azure environment variables are not set.
        FileNotFoundError: If the image file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Document image not found: {file_path}")

    image_bytes = read_image_bytes(file_path)
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": image_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    normalized = normalize_ocr_text_result(result)
    return normalized


def extract_text_from_bytes(
    image_bytes: bytes,
    model_id: str = AZURE_OCR_MODEL_ID,
) -> DocumentTextResult:
    """
    Extract plain text from image bytes using Azure AI Document Intelligence.

    Args:
        image_bytes: Raw bytes of the document image.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-read'.

    Returns:
        DocumentTextResult: Normalized OCR result containing full text and text blocks.
    """
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": image_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    normalized = normalize_ocr_text_result(result)
    return normalized
