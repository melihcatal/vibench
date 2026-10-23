import re
from .document_client import DocumentClient
from .document_models import OCRRequest, ProviderResponse

# Structured field extraction from OCR-normalized text
# Current implementation uses simple regex patterns


def extract_fields(ocr_text: str) -> dict:
    """Very basic extraction of common form fields from OCR text.

    Looks for patterns like "Name:", "Address:", "Phone:", "Email:", and any
    key-value pairs where the key contains a colon. Returns a dict of extracted values.
    """
    fields = {}
    # Basic key/value pairs separated by colon
    for line in ocr_text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    # Specific field patterns
    phone_match = re.search(r"Phone[:\s]*([\d\-\(\)\.]+)", ocr_text, re.IGNORECASE)
    if phone_match:
        fields["Phone"] = phone_match.group(1).strip()
    email_match = re.search(r"Email[:\s]*([\w\.@]+)", ocr_text, re.IGNORECASE)
    if email_match:
        fields["Email"] = email_match.group(1).strip()
    # TODO: Add more sophisticated parsers (e.g., date extraction, tables) as needed
    return fields
