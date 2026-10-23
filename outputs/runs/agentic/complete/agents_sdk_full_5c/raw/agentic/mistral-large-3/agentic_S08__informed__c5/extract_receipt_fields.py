import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import ReceiptExtractionResponse


def extract_receipt_fields(file_path: str, mime_type: str) -> ReceiptExtractionResponse:
    client = get_document_ai_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = "us"
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")  # Prebuilt receipt processor
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(file_path, "rb") as f:
        request = {
            "name": processor_name,
            "raw_document": {
                "content": f.read(),
                "mime_type": mime_type
            }
        }
        result = client.process_document(request=request)

    document = result.document
    fields = {}

    fields["merchant"] = document.entities[0].properties[0].text_anchor.content if document.entities else ""
    fields["tax"] = next(
        (entity.normalized_value.text for entity in document.entities if entity.type_ == "tax"),
        ""
    )
    fields["total"] = next(
        (entity.normalized_value.text for entity in document.entities if entity.type_ == "total"),
        ""
    )
    fields["items"] = [
        {
            "description": item.properties[0].text_anchor.content,
            "price": item.properties[1].normalized_value.text
        }
        for item in document.entities if item.type_ == "line_item"
    ]

    return ReceiptExtractionResponse(
        raw_fields=fields,
        confidence=document.confidence,
        model_used="pretrained-receipt-v1.0-2023-10-30"
    )