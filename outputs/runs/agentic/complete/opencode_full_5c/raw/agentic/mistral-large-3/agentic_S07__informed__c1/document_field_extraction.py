import os
import re
from typing import Dict, List, Optional


def extract_fields(
    text: str, field_patterns: Dict[str, str]
) -> Dict[str, Optional[str]]:
    """
    Extracts structured fields from OCR-normalized document text using regex patterns.
    """
    extracted_fields = {}

    for field_name, pattern in field_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        extracted_fields[field_name] = match.group(1).strip() if match else None

    return extracted_fields
