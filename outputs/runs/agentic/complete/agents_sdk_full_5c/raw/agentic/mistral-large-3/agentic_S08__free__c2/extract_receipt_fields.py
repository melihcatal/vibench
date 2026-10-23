import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import ReceiptFields


def extract_receipt_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    """Extract merchant, tax, total, and items from a receipt using Google Document AI."""
    client = get_document_client()
    processor_name = os.getenv(
        "GOOGLE_DOCUMENT_AI_RECEIPT_PROCESSOR",
        "projects/123/locations/us/processors/789"
    )

    with open(file_path, "rb") as file:
        document = {"content": file.read(), "mime_type": mime_type}

    request = {"name": processor_name, "raw_document": document}
    result = client.process_document(request=request)
    document = result.document

    fields = {
        "merchant": document.entities.get("merchant_name", [{}])[0].get("mention_text", ""),
        "tax": document.entities.get("tax_amount", [{}])[0].get("mention_text", ""),
        "total": document.entities.get("total_amount", [{}])[0].get("mention_text", ""),
        "items": [
            {
                "description": item.get("description", ""),
                "price": item.get("price", "")
            }
            for item in document.entities.get("items", [])
        ]
    }

    return ReceiptFields(**fields).dict()