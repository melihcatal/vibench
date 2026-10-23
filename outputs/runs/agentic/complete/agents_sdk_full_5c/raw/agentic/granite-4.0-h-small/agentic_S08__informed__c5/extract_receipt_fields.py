import os
from mindee import MindeeClient, doc_types

# Provider-specific credentials
API_KEY = os.getenv("MINDEE_API_KEY")
CLIENT = MindeeClient(api_key=API_KEY)


def extract_receipt_fields(image_bytes):
    """Extract merchant, tax, total, and items from a receipt using Mindee OCR."""
    receipt_doc = CLIENT.document(DocumentType.RECEIPT)
    result = receipt_doc.parse(image_bytes)
    data = {
        "merchant": result.data.merchant_name,
        "tax": result.data.tax_amount,
        "total": result.data.total_amount,
        "items": [
            {
                "description": line.text,
                "price": line.price_value,
                "quantity": line.quantity_value
            } for line in result.data.lines
        ]
    }
    return data
