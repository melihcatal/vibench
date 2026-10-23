import os
import json
from pathlib import Path

# Helper to load environment variables for Azure Document Intelligence prebuilt invoice SDK
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")


def extract_receipt_fields(file_path: str) -> dict:
    """Extract merchant, tax, total, and items from a receipt using Azure Document Intelligence.

    Returns a dict with keys: merchant, tax, total, items.
    """
    # Placeholder for SDK call – instantiate the Azure Document Intelligence client
    # and call the prebuilt receipt analysis API.
    # This stub simulates a successful response.
    return {
        "merchant": "Corner Store",
        "tax": 8.75,
        "total": 62.30,
        "items": [
            {"name": "Coffee", "price": 2.5, "quantity": 2},
            {"name": "Muffin", "price": 3.0, "quantity": 1},
        ],
    }
