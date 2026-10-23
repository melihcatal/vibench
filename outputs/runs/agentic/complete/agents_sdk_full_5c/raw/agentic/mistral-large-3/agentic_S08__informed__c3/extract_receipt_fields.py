import os
from typing import Dict, Any
from document_client import get_document_client
from document_models import ReceiptResponse


def extract_receipt_fields(file_path: str) -> ReceiptResponse:
    """
    Extracts merchant, tax, total, and items from a receipt using Google Document AI.
    """
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

    client = get_document_client("google", processor_id=processor_id, location=location, project_id=project_id)

    with open(file_path, "rb") as f:
        content = f.read()

    response = client.process_document(request={
        "name": f"projects/{project_id}/locations/{location}/processors/{processor_id}",
        "raw_document": {"content": content, "mime_type": "application/pdf"}
    })

    document = response.document
    receipt_data: Dict[str, Any] = {
        "merchant": document.text.split("\n")[0] if document.text else "",
        "tax": 0.0,
        "total": 0.0,
        "items": [],
        "confidence": document.confidence,
    }

    for entity in document.entities:
        if entity.type_ == "total_amount":
            receipt_data["total"] = float(entity.mention_text)
        elif entity.type_ == "tax_amount":
            receipt_data["tax"] = float(entity.mention_text)
        elif entity.type_ == "line_item":
            receipt_data["items"].append({
                "description": entity.properties[0].mention_text if entity.properties else "",
                "amount": float(entity.properties[1].mention_text) if len(entity.properties) > 1 else 0.0,
            })

    return ReceiptResponse(**receipt_data)