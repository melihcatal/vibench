from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential
import os
from typing import Optional
from document_models import OCRResponse


def extract_text(image_path: str, mime_type: str = "image/jpeg") -> OCRResponse:
    """
    Extracts plain text from a scanned document image using Azure Document Intelligence.

    Args:
        image_path: Path to the document image file or URL.
        mime_type: MIME type of the document (e.g., "image/jpeg", "image/png").

    Returns:
        OCRResponse: Normalized response containing extracted text and metadata.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type,
            output_content_format=ContentFormat.TEXT,
        )

    result = poller.result()

    return OCRResponse(
        text=result.content,
        pages=len(result.pages) if result.pages else 0,
        language=result.language if result.language else "unknown",
    )
