from typing import Dict, List
import re
from document_models import FieldExtractionResponse


def extract_fields_from_text(
    text: str, field_patterns: Dict[str, str]
) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized document text using regex patterns."""
    fields = {}
    confidence_scores = {}

    for field_name, pattern in field_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field_name] = match.group(1).strip()
            confidence_scores[field_name] = 0.9  # Simulated confidence
        else:
            fields[field_name] = ""
            confidence_scores[field_name] = 0.0

    return FieldExtractionResponse(fields=fields, confidence_scores=confidence_scores)
