import requests
import json
from mindee import MindeeClient, InvoiceV4


def extract_receipt_fields(image_bytes):
    """Extracts merchant, tax, total, and items from a receipt using Mindee Invoice OCR.
    Args:
        image_bytes (bytes): Image file bytes (JPEG/PNG).
    Returns:
        dict: Dictionary containing extracted fields.
    """
    client = MindeeClient(api_key="YOUR_MINDEE_API_KEY")
    invoice = InvoiceV4(client=client)
    result = invoice.parse(file=image_bytes)
    output = result.original_doc.data
    receipt = {
        "merchant": output["merchant"]["name"],
        "tax": output.get("tax", {}).get("total") or "",
        "total": output.get("total", {}).get("amount") or "",
        "items": [
            {
                "description": line.get("description"),
                "quantity": line.get("quantity"),
                "amount": line.get("amount"),
            }
            for line in output.get("items", [])
        ],
    }
    return receipt
