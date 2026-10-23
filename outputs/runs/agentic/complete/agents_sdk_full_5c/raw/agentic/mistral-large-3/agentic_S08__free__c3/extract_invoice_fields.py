import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import InvoiceExtractionResponse


def extract_invoice_fields(file_path: str, mime_type: str) -> InvoiceExtractionResponse:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GCP_PROJECT_ID')}/locations/{os.getenv('GCP_LOCATION')}/processors/{os.getenv('GCP_INVOICE_PROCESSOR_ID')}"

    with open(file_path, "rb") as file:
        content = file.read()

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(content=content, mime_type=mime_type)
    )

    result = client.process_document(request=request)
    document = result.document

    fields = {
        "vendor": document.entities.get("vendor_name", "").strip(),
        "date": document.entities.get("invoice_date", "").strip(),
        "total": float(document.entities.get("total_amount", 0.0)),
        "line_items": []
    }

    for entity in document.entities:
        if entity.type_ == "line_item":
            fields["line_items"].append({
                "description": entity.properties.get("description", "").strip(),
                "amount": float(entity.properties.get("amount", 0.0))
            })

    return InvoiceExtractionResponse(**fields)