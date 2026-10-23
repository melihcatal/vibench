import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_client
from document_models import ReceiptExtractionResponse


def extract_receipt_fields(file_path: str, mime_type: str) -> ReceiptExtractionResponse:
    client = get_document_client()
    processor_name = f"projects/{os.getenv('GCP_PROJECT_ID')}/locations/{os.getenv('GCP_LOCATION')}/processors/{os.getenv('GCP_RECEIPT_PROCESSOR_ID')}"

    with open(file_path, "rb") as file:
        content = file.read()

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(content=content, mime_type=mime_type)
    )

    result = client.process_document(request=request)
    document = result.document

    fields = {
        "merchant": document.entities.get("merchant_name", "").strip(),
        "tax": float(document.entities.get("tax_amount", 0.0)),
        "total": float(document.entities.get("total_amount", 0.0)),
        "items": []
    }

    for entity in document.entities:
        if entity.type_ == "item":
            fields["items"].append({
                "description": entity.properties.get("description", "").strip(),
                "price": float(entity.properties.get("price", 0.0))
            })

    return ReceiptExtractionResponse(**fields)