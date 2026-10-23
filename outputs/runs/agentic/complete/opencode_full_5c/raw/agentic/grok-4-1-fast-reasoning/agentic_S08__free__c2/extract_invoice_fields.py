import os
from google.cloud import documentai_v1 as documentai
from document_client import load_document
from typing import Dict, Any
import json


def extract_invoice_fields(image_path: str) -> Dict[str, Any]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = "86fb8469ce501dfe"  # Concrete Document AI invoice processor ID

    client = documentai.DocumentProcessorServiceClient()

    document_bytes, mime_type = load_document(image_path)

    request = documentai.ProcessRequest(
        name=f"projects/{project_id}/locations/{location}/processors/{processor_id}",
        raw_document=documentai.RawDocument(
            content=document_bytes, mime_type=mime_type
        ),
    )

    result = client.process_request(request=request)
    document = result.document
    entities = document.entities

    vendor = ""
    date = ""
    total = 0.0
    line_items = []
    confidence = {}

    for entity in entities:
        confidence[entity.type_] = entity.confidence
        if entity.type_ == "supplier_organization_name":
            vendor = entity.mention_text
        elif entity.type_ == "invoice_date":
            date = entity.mention_text
        elif entity.type_ == "total_invoice_amount":
            total = float(entity.mention_text)
        elif entity.type_ == "line_item/description":
            line_items.append({"description": entity.mention_text, "amount": 0.0})

    return {
        "vendor": vendor,
        "date": date,
        "total": total,
        "line_items": line_items,
        "confidence": confidence,
    }
