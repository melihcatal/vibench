# document_field_extraction.py
# LATER-STEP file
# Extracts structured fields from OCR-normalized text (placeholder implementation)

import re
from document_models import FieldExtractionResult


def extract_fields(ocr_text: str) -> List[FieldExtractionResult]:
    """Dummy parser that extracts a few common form fields from plain text.

    Args:
        ocr_text: Full text extracted by OCR.

    Returns:
        List of FieldExtractionResult objects with detected key/value pairs.
    """
    results = []
    # Simple regex patterns for demonstration
    patterns = {
        "Date": r"(?i)date[:\s]*([0-9\/\-]+)",
        "Amount": r"(?i)total[:\s]*([\$\xa3]?\d+(?:\.\d{2})?)",
        "Name": r"(?i)name[:\s]*([A-Za-z]+(?:\s[A-Za-z]+)?)",
    }
    for name, pattern in patterns.items():
        match = re.search(pattern, ocr_text)
        if match:
            value = match.group(1)
            results.append(
                FieldExtractionResult(
                    field_name=name, value=value.strip(), confidence=0.9
                )
            )
    return results
