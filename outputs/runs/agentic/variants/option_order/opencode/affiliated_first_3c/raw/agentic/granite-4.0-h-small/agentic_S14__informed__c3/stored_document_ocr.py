import os
import json
from storage_client import StorageClient, ObjectMetadataResponse
from storage_models import (
    OCRResponse,
    TranslateRequest,
    SummarizeRequest,
    EmbedRequest,
    EmbedResponse,
)
from typing import Any, Dict

PROVIDER = "Azure Document Intelligence"


# Placeholder client wrapper around Azure Document Intelligence SDK
# In production you would import the real SDK (azure-ai-documentintelligence)
class OcrClient:
    """Stub client for Azure Document Intelligence OCR API."""

    def __init__(self):
        # Required environment variables for auth
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        # Placeholder for SDK client instantiation
        self.client = None

    def analyze_document(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Call Azure Document Intelligence layout/OCR API."""
        # Placeholder implementation – in real code you would call the SDK's analyze API
        # Returning a mock structure that contains a 'text' field with extracted text
        return {"text": "Sample text extracted from the PDF."}


# Initialise the stub client
ocr = OcrClient()


def run_ocr_on_stored_document(bucket_name: str, key: str) -> OCRResponse:
    """
    Download the object, run OCR/Document Intelligence, and return plain text.

    Args:
        bucket_name (str): Bucket containing the PDF/binary document.
        key (str): Object path/key.
    Returns:
        OCRResponse: Contains the extracted plain text.
    """
    # Simulate download (in real code use client.download or streaming)
    print(f"[{PROVIDER}] Downloading document {bucket_name}/{key} for OCR")
    # For demonstration we pretend the object is a PDF and embed sample bytes
    pdf_bytes = b"PDF content placeholder"
    raw_response = ocr.analyze_document(pdf_bytes)
    extracted_text = raw_response.get("text", "")
    print(f"[{PROVIDER}] OCR extracted text ({len(extracted_text)} chars)")
    return OCRResponse(raw=raw_response)


# If executed directly, run a quick sanity test
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: stored_document_ocr.py <bucket> <key>")
        sys.exit(1)
    ocr_result = run_ocr_on_stored_document(sys.argv[1], sys.argv[2])
    print(ocr_result.raw)
