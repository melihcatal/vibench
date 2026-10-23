import os
from typing import Optional, Dict, Any
import base64
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_client
from document_models import DocumentResponse, TextExtractionResult


def extract_text(
    image_path: str, language: Optional[str] = None
) -> TextExtractionResult:
    """
    Extract plain text from a scanned document image using Azure Form Recognizer.

    Args:
        image_path: Path to the image file
        language: Optional language hint for OCR (e.g., 'en', 'es')

    Returns:
        TextExtractionResult containing extracted text and metadata
    """
    client = get_azure_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-read", document=image_data, locale=language
    )

    result = poller.result()

    full_text = ""
    for page in result.pages:
        for line in page.lines:
            full_text += line.content + "\n"

    return TextExtractionResult(
        text=full_text.strip(),
        language=language,
        provider="azure_form_recognizer",
        model_id="prebuilt-read",
        confidence=result.api_version,
    )
