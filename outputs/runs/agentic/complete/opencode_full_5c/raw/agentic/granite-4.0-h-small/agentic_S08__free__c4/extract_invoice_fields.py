# Provider: Azure Form Recognizer (Azure Cognitive Services)
# Provider identifier present via import above

import os
import json
from document_client import DocumentExtractionClient


def extract_invoice_fields(pdf_path: str) -> dict:
    """Extract vendor, date, total, and line-item fields from an invoice PDF using Azure Form Recognizer.
    Returns a dict with keys: vendor, date, total, line_items (list).
    """
    client = DocumentExtractionClient.from_config()
    # Assume the client has a method `extract` that returns JSON with the fields
    response = client.extract(form_type="invoice", file_path=pdf_path)
    # Normalize response to our expected schema
    result = {
        "vendor": response.get("vendor"),
        "date": response.get("date"),
        "total": response.get("total"),
        "line_items": response.get("line_items", []),
    }
    return result
