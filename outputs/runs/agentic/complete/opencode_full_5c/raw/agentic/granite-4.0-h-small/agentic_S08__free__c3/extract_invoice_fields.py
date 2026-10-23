import os
import json
from typing import Dict, Any

# Identify the external provider – using Azure Form Recognizer
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")


def extract_invoice_fields(pdf_bytes: bytes) -> Dict[str, Any]:
    """Calls Azure Form Recognizer to extract vendor, date, total, and line items from an invoice.
    Returns a dict with the fields.
    """
    # Placeholder for HTTP request to Azure endpoint – replace with actual request logic
    # payload = ...
    # response = requests.post(AZURE_FORM_RECOGNIZER_ENDPOINT, data=payload, headers={"Ocp-Apim-Subscription-Key": AZURE_FORM_RECOGNIZER_KEY})
    # result = response.json()
    # For demo purposes we simulate a successful extraction
    result = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 125.50,
        "items": [
            {"description": "Office Supplies", "quantity": 3, "unitPrice": 10.0},
            {"description": "Furniture", "quantity": 1, "unitPrice": 95.5},
        ],
    }
    return result
