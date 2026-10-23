import os
from typing import TypedDict, List
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import FieldExtractionRequest, FieldExtractionResponse

# Structured field extraction example using a pre-built model or custom NLP


def extract_fields(request: FieldExtractionRequest) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized document text."""
    # Supported downstream extractors (Amazon Textract AnalyzeExpense, Mindee Invoice, etc.)
    # This example demonstrates a generic approach: simple regex/key lookup
    text = request["text"]
    service = request["service"].lower()
    fields = {}
    confidence = 0.90

    if service == "textract-analyzeexpense":
        # Placeholder: would call Textract AnalyzeExpense SDK here
        # For demo, look for common expense fields in OCR text
        if "TOTAL" in text.upper():
            fields["Total"] = "$123.45"  # dummy value
        if "VAT" in text.upper():
            fields["VAT"] = "12.34%"
    elif service == "invoice-ocr":
        # Mindee / Alibaba invoice OCR placeholder
        if "INVOICE NUMBER" in text.upper():
            fields["Invoice Number"] = "INV-001"
        if "TOTAL AMOUNT" in text.upper():
            fields["Total Amount"] = "$250.00"
        if "DUE DATE" in text.upper():
            fields["Due Date"] = "2025-12-31"
    else:
        # Fallback: naive regex extraction of key-value patterns
        lines = text.splitlines()
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
    return FieldExtractionResponse(fields=fields, confidence=confidence)


# Data model
class FieldExtractionRequest(TypedDict):
    text: str
    service: Literal[
        "textract-analyzeexpense",
        "invoice-ocr",
        # Extend with other providers as needed
    ]


class FieldExtractionResponse(TypedDict):
    fields: dict
    confidence: float
