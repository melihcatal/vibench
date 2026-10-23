import os
from typing import Optional
from document_client import get_document_client
from document_models import TextExtractionResponse


def extract_text(image_path: str, mime_type: Optional[str] = None) -> TextExtractionResponse:
    """
    Extract plain text from a scanned document image using Azure AI Document Intelligence.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        analyze_request=image_data,
        content_type="application/octet-stream"
    )
    result = poller.result()

    extracted_text = "\n".join([line.content for line in result.pages[0].lines])
    return TextExtractionResponse(
        text=extracted_text,
        pages=len(result.pages),
        language=result.pages[0].language if result.pages and result.pages[0].language else None
    )