# [LATER-STEP] document_field_extraction.py
"""Extract structured fields from OCR-normalized document text."""

import json
from typing import Dict
from document_client import OCRClient
from document_models import OCRRequest, OCRResponse


# Placeholder field extractor (replace with provider models like AWS Textract Forms, Azure Form Recognizer)
def simple_field_extractor(text: str) -> Dict[str, str]:
    """Naive extractor that looks for lines starting with known keys.

    Returns a dictionary mapping field names to their values.
    """
    fields = {}
    for line in text.splitlines():
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def extract_fields(image_path: str) -> Dict[str, str]:
    """End‑to‑end extraction of structured fields from a document image.

    Args:
        image_path: Path to a scanned image file.

    Returns:
        Dictionary of extracted key/value pairs.
    """
    # 1️⃣ OCR extraction
    ocr_response: OCRResponse = OCR_CLIENT.extract_text(image_path)
    # 2️⃣ Simple key‑value parsing
    fields = simple_field_extractor(ocr_response.text)
    return fields


# Example usage (disabled)
# if __name__ == '__main__':
#     fields = extract_fields('sample_form.png')
#     print(json.dumps(fields, indent=2))
