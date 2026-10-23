import re
from typing import List, Dict, Any

# Utility to extract structured fields from normalized OCR output


def extract_fields(normalized: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract key‑value pairs from OCR text using simple regex‑based heuristics.

    Args:
        normalized (Dict[str, Any]): Normalized OCR payload containing a 'text' field.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with 'field' and 'value' keys.
    """
    text = normalized.get("text", "")
    # Example patterns for common form fields
    patterns = {
        "Date": r"Date[:\s]*(.+?)\\n",
        "Amount": r"Amount[:\s]*\$?([0-9,.]+)\\n",
        "Invoice Number": r"Invoice Number[:\s]*(.+)\\n",
    }
    extracted: List[Dict[str, Any]] = []
    for name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            extracted.append({"field": name, "value": value})
    return extracted
