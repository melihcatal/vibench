from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
import os
from typing import Dict, Any, Optional
from document_models import KeyValueResponse


def document_field_extraction(
    image_path: str, mime_type: str = "image/jpeg"
) -> Dict[str, Any]:
    """
    Extracts structured fields from OCR-normalized document text using Azure Document Intelligence prebuilt-invoice.

    Args:
        image_path: Path to the document image file or URL.
        mime_type: MIME type of the document (e.g., "image/jpeg", "image/png").

    Returns:
        Dictionary containing extracted structured fields.
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
            "prebuilt-invoice",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type,
        )

    result: AnalyzeResult = poller.result()

    fields = {}
    if result.documents:
        for name, field in result.documents[0].fields.items():
            fields[name] = {
                "value": field.value if field.value else None,
                "confidence": field.confidence,
            }

    return fields
