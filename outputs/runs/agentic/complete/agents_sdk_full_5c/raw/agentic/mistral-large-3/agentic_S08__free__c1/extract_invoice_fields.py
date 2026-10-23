import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import InvoiceExtractionResponse


def extract_invoice_fields(file_path: str, mime_type: str) -> InvoiceExtractionResponse:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/4f8d2e1a3b5c6d7e"

    with open(file_path, "rb") as file:
        content = file.read()

    request = {
        "name": processor_name,
        "raw_document": {
            "content": content,
            "mime_type": mime_type,
        },
    }

    result = client.process_document(request=request)
    document = result.document

    fields = {
        "vendor": document.entities[0].properties[0].text_anchor.content if document.entities else "",
        "date": document.entities[1].properties[0].text_anchor.content if len(document.entities) > 1 else "",
        "total": document.entities[2].properties[0].text_anchor.content if len(document.entities) > 2 else "",
        "line_items": [
            {
                "description": item.properties[0].text_anchor.content,
                "amount": item.properties[1].text_anchor.content,
            }
            for item in document.entities[3].properties if len(document.entities) > 3
        ],
    }

    return InvoiceExtractionResponse(**fields)