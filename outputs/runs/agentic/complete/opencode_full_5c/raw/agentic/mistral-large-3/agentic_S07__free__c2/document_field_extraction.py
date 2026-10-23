from typing import Dict, List, Optional
import re
from pydantic import BaseModel
from document_client import get_document_client
from document_models import OCRResponse


class FieldExtractionResult(BaseModel):
    fields: Dict[str, str]
    confidence: Dict[str, float]


def extract_fields_from_text(text: str) -> FieldExtractionResult:
    """Extract structured fields from OCR-normalized document text using regex patterns."""
    patterns = {
        "invoice_number": r"Invoice\s*(?:No\.?|Number)?\s*[:#]?\s*([A-Z0-9-]+)",
        "date": r"Date\s*[:#]?\s*(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})",
        "total_amount": r"Total\s*(?:Amount)?\s*[:#]?\s*\$?([0-9,.]+)",
        "vendor_name": r"Vendor\s*(?:Name)?\s*[:#]?\s*([A-Za-z\s&]+)",
        "customer_name": r"Customer\s*(?:Name)?\s*[:#]?\s*([A-Za-z\s]+)",
    }

    fields = {}
    confidence = {}

    for field_name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field_name] = match.group(1).strip()
            confidence[field_name] = 0.9  # Simulated confidence
        else:
            confidence[field_name] = 0.0

    return FieldExtractionResult(fields=fields, confidence=confidence)


def document_field_extraction(image_path: str) -> FieldExtractionResult:
    """Extract structured fields from OCR-normalized document text."""
    from extract_text import extract_text

    ocr_result = extract_text(image_path)
    return extract_fields_from_text(ocr_result.text)
