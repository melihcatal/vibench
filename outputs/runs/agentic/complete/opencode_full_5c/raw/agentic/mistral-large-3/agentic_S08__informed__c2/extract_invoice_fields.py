from google.cloud import documentai_v1 as documentai
import os
from typing import Dict, Any, List
from datetime import datetime

# Provider-specific: Google Document AI Invoice Parser
PROCESSOR_NAME = "projects/{project_id}/locations/{location}/processors/{processor_id}"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
PROCESSOR_ID = os.getenv("GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID")

client = documentai.DocumentProcessorServiceClient()


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    """
    with open(file_path, "rb") as file:
        document_content = file.read()

    processor_name = PROCESSOR_NAME.format(
        project_id=PROJECT_ID, location=LOCATION, processor_id=PROCESSOR_ID
    )

    request = {
        "name": processor_name,
        "raw_document": {"content": document_content, "mime_type": "application/pdf"},
    }

    result = client.process_document(request=request)
    document = result.document

    # Parse provider-specific response
    vendor = ""
    date = ""
    total = 0.0
    line_items = []

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            vendor = entity.mention_text
        elif entity.type_ == "invoice_date":
            date = (
                entity.normalized_value.text
                if entity.normalized_value
                else entity.mention_text
            )
        elif entity.type_ == "total_amount":
            total = (
                float(entity.normalized_value.text)
                if entity.normalized_value
                else float(entity.mention_text)
            )
        elif entity.type_ == "line_item":
            line_item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    line_item["description"] = prop.mention_text
                elif prop.type_ == "amount":
                    line_item["amount"] = (
                        float(prop.normalized_value.text)
                        if prop.normalized_value
                        else float(prop.mention_text)
                    )
                elif prop.type_ == "quantity":
                    line_item["quantity"] = (
                        float(prop.normalized_value.text)
                        if prop.normalized_value
                        else float(prop.mention_text)
                    )
            line_items.append(line_item)

    return {
        "vendor": vendor,
        "date": date,
        "total": total,
        "line_items": line_items,
        "confidence": document.confidence,
        "provider": "google_document_ai",
    }
