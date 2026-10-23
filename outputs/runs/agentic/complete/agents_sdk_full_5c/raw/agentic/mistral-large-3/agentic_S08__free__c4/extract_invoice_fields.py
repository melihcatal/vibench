import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import InvoiceFields


def extract_invoice_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/4f8d5e7c1b3a9d2e"

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

    invoice_data = {
        "vendor": document.entities[0].properties[0].mention_text if document.entities else "",
        "date": document.entities[1].mention_text if len(document.entities) > 1 else "",
        "total": document.entities[2].mention_text if len(document.entities) > 2 else "",
        "line_items": []
    }

    for entity in document.entities:
        if entity.type_ == "line_item":
            invoice_data["line_items"].append({
                "description": entity.properties[0].mention_text,
                "amount": entity.properties[1].mention_text
            })

    return InvoiceFields(**invoice_data).dict()