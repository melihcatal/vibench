import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import ReceiptFields


def extract_receipt_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/7f3a9d1c5e8b2d4f"

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
        "merchant": document.entities[0].mention_text if document.entities else "",
        "tax": document.entities[1].mention_text if len(document.entities) > 1 else "",
        "total": document.entities[2].mention_text if len(document.entities) > 2 else "",
        "items": []
    }

    for entity in document.entities:
        if entity.type_ == "item":
            receipt_data["items"].append({
                "name": entity.properties[0].mention_text,
                "price": entity.properties[1].mention_text
            })

    return ReceiptFields(**receipt_data).dict()