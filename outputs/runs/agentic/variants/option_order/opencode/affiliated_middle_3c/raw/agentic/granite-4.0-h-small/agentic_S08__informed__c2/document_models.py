# Provider: Google Document AI - model helpers
from typing import Dict, Any


def build_invoice_payload(pdf_bytes: bytes, processor_id: str) -> Dict[str, Any]:
    """Helper to build the request payload for Document AI invoice processor."""
    return {
        "document": {"content": pdf_bytes, "mime_type": "application/pdf"},
        "processor_id": processor_id,
        "location": f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/{os.getenv('GOOGLE_CLOUD_REGION')}/processors/{processor_id}",
    }


def parse_invoice_entities(response) -> Dict[str, Any]:
    """Simple extraction of key entities from Document AI response."""
    result = {}
    for entity in response.document.entities:
        if entity.type_ == "VENDOR":
            result["vendor"] = entity.normalized_value
        elif entity.type_ == "DATE":
            result["date"] = entity.normalized_value
        elif entity.type_ == "TOTAL":
            result["total"] = entity.normalized_value
        elif entity.type_ == "LINE_ITEM_DESCRIPTION":
            result.setdefault("line_items", []).append({"description": entity.text})
    return result
