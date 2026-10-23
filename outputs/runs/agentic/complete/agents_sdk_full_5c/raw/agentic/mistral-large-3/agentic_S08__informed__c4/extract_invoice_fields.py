from typing import Dict, Any
import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import InvoiceExtractionResponse


def extract_invoice_fields(file_path: str, mime_type: str) -> InvoiceExtractionResponse:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI Invoice Parser.
    """
    client = get_document_client("documentai")
    processor_name = "projects/{project_id}/locations/{location}/processors/{processor_id}".format(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us"),
        processor_id=os.getenv("GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID")
    )

    with open(file_path, "rb") as file:
        document = {"content": file.read(), "mime_type": mime_type}

    request = {"name": processor_name, "raw_document": document}
    result = client.process_document(request=request)
    document = result.document

    fields = {
        "vendor": document.entities.get("supplier_name", [{}])[0].get("mention_text", ""),
        "date": document.entities.get("invoice_date", [{}])[0].get("mention_text", ""),
        "total": document.entities.get("total_amount", [{}])[0].get("mention_text", ""),
        "line_items": []
    }

    for item in document.entities.get("line_item", []):
        line_item = {
            "description": item.get("description", ""),
            "amount": item.get("amount", "")
        }
        fields["line_items"].append(line_item)

    return InvoiceExtractionResponse(**fields)