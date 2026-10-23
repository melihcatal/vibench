"""
Extract plain text from a scanned document image using Azure AI Document Intelligence.

Uses the azure-ai-documentintelligence SDK to perform OCR on document images
and returns the extracted plain text content.
"""

from typing import Optional

from document_client import create_document_intelligence_client, read_file_bytes
from document_models import OcrTextResponse, normalize_azure_di_text_response


def extract_text_from_image(
    file_path: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> OcrTextResponse:
    """
    Extract plain text from a scanned document image using Azure Document Intelligence OCR.

    Args:
        file_path: Path to the local document image file (PDF, PNG, JPEG, TIFF, etc.).
        endpoint: Azure DI endpoint URL. Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT.
        key: Azure DI API key. Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY.

    Returns:
        OcrTextResponse containing the extracted full text and per-block text segments.
    """
    client = create_document_intelligence_client(endpoint=endpoint, key=key)
    file_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=file_bytes,
    )
    result = poller.result()
    result_dict = result.as_dict()

    return normalize_azure_di_text_response(result_dict)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resp = extract_text_from_image(sys.argv[1])
        print(resp.full_text)
    else:
        print("Usage: python extract_text.py <path-to-document>")
