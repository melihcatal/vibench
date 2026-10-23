from typing import Dict, List, Optional
import re
from document_models import OCRResponse


def extract_fields(ocr_response: OCRResponse) -> Dict[str, str]:
    """Extract structured fields from OCR-normalized document text using regex patterns."""
    text = ocr_response.text
    fields = {}

    # Extract common fields using regex
    patterns = {
        "date": r"\b(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b",
        "invoice_number": r"\b(INV|Invoice)[- ]?(\d{4,10})\b",
        "total_amount": r"\bTotal[: ]?\$?([0-9]+\.[0-9]{2})\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b",
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field] = (
                match.group(1) if field != "invoice_number" else match.group(2)
            )

    return fields


def document_field_extraction(ocr_response: OCRResponse) -> Dict[str, str]:
    """Extract structured fields from OCR-normalized document text."""
    return extract_fields(ocr_response)
