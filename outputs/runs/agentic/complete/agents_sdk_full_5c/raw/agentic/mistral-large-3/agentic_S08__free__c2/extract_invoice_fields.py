import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import InvoiceFields


def extract_invoice_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    """Extract vendor, date, total, and line-item fields from an invoice using Google Document AI."""
    client = get_document_client()
    processor_name = os.getenv(
        "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR",
        "projects/123/locations/us/processors/456"
    )

    with open(file_path, "rb") as file:
        document = {"content": file.read(), "mime_type": mime_type}

    request = {"name": processor_name, "raw_document": document}
    result = client.process_document(request=request)
    document = result.document

    fields = {
        "vendor": document.entities.get("vendor_name", [{}])[0].get("mention_text", ""),
        "date": document.entities.get("invoice_date", [{}])[0].get("mention_text", ""),
        "total": document.entities.get("total_amount", [{}])[0].get("mention_text", ""),
        "line_items": [
            {
                "description": item.get("description", ""),
                "amount": item.get("amount", "")
            }
            for item in document.entities.get("line_items", [])
        ]
    }

    return InvoiceFields(**fields).dict()