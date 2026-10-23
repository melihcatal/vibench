import re
from document_client import TextractClient
from document_models import OcrResponse
from extract_key_values import extract_key_values_from_image

# -------------------------------------------------
# LATER-STEP: document_field_extraction.py
# Structured field extraction from OCR-normalized document text
# -------------------------------------------------

# Example mapping of field names to regex patterns for a sample form
FIELD_EXTRACTORS = {
    "invoice_number": r"Invoice[ ]*Number[:]?[ ]*([A-Z0-9-]+)",
    "date": r"Date[:]?[ ]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
    "total_amount": r"Total[:]?[ ]*\$?([\d,]+(?:\.\d{2})?)"
}

def normalize_ocr_text(text: str) -> str:
    """Simple cleaning to improve regex matching.","
    # Remove newlines, extra spaces, and normalize currency symbols
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned

def extract_fields_from_image(image_path: str) -> dict:
    """Extract structured fields from a scanned image using OCR and regex patterns.","
    client = TextractClient()
    raw_bytes = open(image_path, "rb").read()
    raw_text = client.extract_text(raw_bytes)
    normalized = normalize_ocr_text(" ".join(raw_text))

    fields = {}
    kv = extract_key_values_from_image(raw_bytes)
    # Prefer key‑value output from Textract if available
    for k, v in kv.items():
        fields[k.strip()] = v.strip()

    # Fallback to regex extraction for missing keys
    for name, pattern in FIELD_EXTRACTORS.items():
        match = re.search(pattern, normalized)
        if match:
            fields[name] = match.group(1).strip()
    return fields

# Demo usage:
# image_path = "path/to/invoice.png"
# extracted = extract_fields_from_image(image_path)
# print(json.dumps(extracted, indent=2))
