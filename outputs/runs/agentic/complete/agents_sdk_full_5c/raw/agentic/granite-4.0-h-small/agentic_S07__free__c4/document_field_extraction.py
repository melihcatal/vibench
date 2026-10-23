# [LATER-STEP] document_field_extraction.py

import re
from typing import Dict
from .document_models import TextExtractionResponse, FieldExtractionResponse

def extract_fields(ocr_text: str) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized text using simple regex patterns.

    Args:
        ocr_text: full plain text extracted from a document.
    
    Returns:
        FieldExtractionResponse containing a dict of field_name -> value.
    """
    # Example patterns—extend or replace with more sophisticated NER/DL models as needed
    patterns = {
        "date": r"\\b(\\d{1,2})[/-](\\d{1,2})[/-](\\d{2,4})\\b",
        "amount": r"\\$?\\s*([\d,]+(?:\\.\\d{2})?)",
        "invoice_number": r"INV\\s*[-: ]*(\d+)",
        "client_name": r"Client[:\s]*([A-Za-z ]+)"
    }
    fields = {}
    for name, pat in patterns.items():
        match = re.search(pat, ocr_text, re.IGNORECASE)
        if match:
            fields[name] = match.group(0).strip()
    return FieldExtractionResponse(fields=fields)
