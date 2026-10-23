# extract_key_values.py
# SAME-SCENARIO OCR file
# Uses Mindee Document OCR via mindee SDK

import os
from mindee import MindeeApp, Document

# Configure using MINDEE_API_KEY environment variable
app = MindeeApp(api_key=os.getenv("MINDEE_API_KEY"))


def extract_key_values_from_form(image_path: str) -> dict:
    """Extract key-value pairs from a form-like document using Mindee OCR.

    Args:
        image_path: Local path to the image file.

    Returns:
        Dictionary mapping field names to extracted values.
    """
    doc = Document.from_path(image_path)
    response = app.invoice.parse(doc)
    kv_pairs = {}
    for field in response.parsed_object.fields:
        kv_pairs[field.label] = field.value
    return kv_pairs
