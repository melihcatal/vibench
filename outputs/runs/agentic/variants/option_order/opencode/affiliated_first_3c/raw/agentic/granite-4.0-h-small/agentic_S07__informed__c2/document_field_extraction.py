import os
from typing import List, Dict
from document_client import OcrClient
from document_models import OCRResponse, LayoutResponse


def extract_fields(
    image_path: str, schema: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Extract structured fields from OCR-normalized document text based on a simple schema.

    schema: list of dicts with keys: 'key' (expected field name), 'pattern' (regex pattern or exact match), 'type' (e.g., 'string', 'number').
    Returns a list of dicts representing extracted field values.
    Uses Google Document AI processors to obtain high-quality OCR text.
    """
    client = OcrClient()
    ocr_result: OCRResponse = client.process_document(open(image_path, "rb").read())
    document_text = ocr_result["text"]

    extracted = []
    for field_def in schema:
        key = field_def["key"]
        pattern = field_def.get("pattern", key)
        # Very simple extraction: find first substring matching pattern
        import re

        match = re.search(pattern, document_text, re.IGNORECASE)
        if match:
            value = match.group().strip()
            # Optional type coercion
            if field_def.get("type") == "number":
                try:
                    value = float(value) if "." in value else int(value)
                except ValueError:
                    value = None
            extracted.append({"key": key, "value": value})
    return extracted
