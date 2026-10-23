import os
import json
from typing import Dict, Any

# Identify the external provider – using AWS Textract for receipt analysis
AWS_TEXTRACT_ENDPOINT = os.getenv("AWS_TEXTRACT_ENDPOINT")
AWS_TEXTRACT_KEY = os.getenv("AWS_TEXTRACT_KEY")


def extract_receipt_fields(image_bytes: bytes) -> Dict[str, Any]:
    """Calls AWS Textract to extract merchant, tax, total, and items from a receipt.
    Returns a dict with the fields.
    """
    # Placeholder for AWS Textract API call – replace with real request logic
    # response = requests.post(AWS_TEXTRACT_ENDPOINT, data=image_bytes, headers={"x-amz-target": "TextractAPI.AnalyzeExpense", "Authorization": f"Bearer {AWS_TEXTRACT_KEY}"})
    # result = response.json()
    # Demo extraction
    result = {
        "merchant": "Joe's Diner",
        "tax": 7.25,
        "total": 32.50,
        "items": [
            {"name": "Coffee", "quantity": 2, "price": 1.5},
            {"name": "Bagel", "quantity": 1, "price": 2.0},
        ],
    }
    return result
