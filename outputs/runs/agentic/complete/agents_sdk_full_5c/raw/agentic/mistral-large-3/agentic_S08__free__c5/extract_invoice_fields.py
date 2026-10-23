import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import InvoiceFields


def extract_invoice_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/1234567890abcdef"  # Concrete Google Document AI processor for invoices

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
        "vendor": document.entities.get("vendor_name", [{}])[0].text,
        "date": document.entities.get("invoice_date", [{}])[0].text,
        "total": document.entities.get("total_amount", [{}])[0].text,
        "line_items": []
    }

    for entity in document.entities:
        if entity.type_ == "line_item":
            invoice_data["line_items"].append({
                "description": entity.properties.get("description", [{}])[0].text,
                "amount": entity.properties.get("amount", [{}])[0].text
            })

    return InvoiceFields(**invoice_data).dict()