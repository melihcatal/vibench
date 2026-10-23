import os
from typing import List, TypedDict
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import FieldExtractionRequest, FieldExtractionResponse

# Key-value pair extraction example using Azure Document Intelligence


def extract_key_values(request: FieldExtractionRequest) -> FieldExtractionResponse:
    """Extract structured key-value pairs from a form-like document using OCR and a downstream parsing step."""
    allowed = [
        "azure-document-intelligence",
        "google-document-ai",
        "mindee",
        "amazon-textract",
        "alibaba-ocr",
    ]
    if request["service"].lower() not in allowed:
        raise ValueError(f"service must be one of {allowed}")

    # Step 1: Run OCR on the raw image (or document) to get raw text
    from extract_text import extract_text

    ocr_result = extract_text(request["image"].encode(), service=request["service"])

    # Step 2: Placeholder parsing logic for KVP extraction
    # In a real implementation you would use the chosen provider's prebuilt KV model or custom NLP logic
    key_values = []
    # Example dummy KV extraction from dummy text
    if "Invoice Number" in ocr_result["full_text"]:
        key_values.append({"key": "Invoice Number", "value": "INV-12345"})
    if "Total Amount" in ocr_result["full_text"]:
        key_values.append({"key": "Total Amount", "value": "$99.99"})
    if "Due Date" in ocr_result["full_text"]:
        key_values.append({"key": "Due Date", "value": "2025-12-31"})

    return FieldExtractionResponse(fields=key_values, confidence=0.92)
