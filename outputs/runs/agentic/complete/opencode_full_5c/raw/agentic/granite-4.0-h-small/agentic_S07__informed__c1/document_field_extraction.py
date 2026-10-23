# Structured field extraction from OCR-normalized text
# Uses a simple heuristic parser (placeholder) that could be swapped with a Mindee or Google DI processor later

import re
from typing import Dict, List

# Local response model for a set of extracted fields
FieldExtractionResult = Dict[str, Any]

# Naive parser for invoices / forms (placeholder)


def extract_fields(ocr_text: List[str]) -> FieldExtractionResult:
    """Extract a set of structured key/value pairs from OCR lines."""
    fields = {}
    for line in ocr_text:
        line = line.strip()
        # Simple patterns: "Amount: $123.45" or "Invoice #: 12345"
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        # Email pattern detection
        if "@" in line and not any(char.isdigit() for char in line):
            fields["Email"] = line.strip()
    return fields
