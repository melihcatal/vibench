import os
import json
from pathlib import Path

# Helper to load environment variables for Alibaba Cloud OCR
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


def extract_invoice_fields(file_path: str) -> dict:
    """Extract vendor, date, total, and line-item fields from an invoice using Alibaba Cloud OCR.

    Returns a dict with keys: vendor, date, total, line_items.
    """
    # Placeholder for SDK call – in real code you would instantiate the Alibaba OCR client
    # and call the appropriate invoice recognition API.
    # This stub simulates a successful response.
    return {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 125.50,
        "line_items": [
            {"description": "Widget A", "quantity": 2, "unit_price": 45.0},
            {"description": "Widget B", "quantity": 1, "unit_price": 35.5},
        ],
    }
