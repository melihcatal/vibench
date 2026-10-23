import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import ReceiptFields


def extract_receipt_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/9876543210fedcba"  # Concrete Google Document AI processor for receipts

    with open(file_path, "rb") as file:
        content = file.read()

    request = {
        "name": processor_name,
        "raw_document": {
            "content": content,
            "mime_type": mime_type
        }
    }

    result = client.process_document(request=request)
    document = result.document

    receipt_data = {
        "merchant": document.entities.get("merchant_name", [{}])[0].text,
        "tax": document.entities.get("tax_amount", [{}])[0].text,
        "total": document.entities.get("total_amount", [{}])[0].text,
        "items": []
    }

    for entity in document.entities:
        if entity.type_ == "line_item":
            receipt_data["items"].append({
                "description": entity.properties.get("description", [{}])[0].text,
                "price": entity.properties.get("price", [{}])[0].text
            })

    return ReceiptFields(**receipt_data).dict()