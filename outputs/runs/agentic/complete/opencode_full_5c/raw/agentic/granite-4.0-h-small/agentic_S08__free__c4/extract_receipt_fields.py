# Provider: Google Document AI (Vision AI)
# Provider identifier present via import above

import os
import json
from document_client import DocumentExtractionClient


def extract_receipt_fields(pdf_path: str) -> dict:
    """Extract merchant, tax, total, and items from a receipt PDF using Google Document AI.
    Returns a dict with keys: merchant, tax, total, items (list).
    """
    client = DocumentExtractionClient.from_config()
    response = client.extract(form_type="receipt", file_path=pdf_path)
    result = {
        "merchant": response.get("merchant"),
        "tax": response.get("tax"),
        "total": response.get("total"),
        "items": response.get("items", []),
    }
    return result
