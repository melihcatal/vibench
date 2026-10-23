import json
from typing import Any, Dict, List

from document_client import get_client, load_config, process_content


def extract_receipt_fields(content: bytes, mime_type: str = "application/pdf") -> Dict[str, Any]:
    config = load_config()
    client = get_client()
    document = process_content(client, config, content, mime_type)
    entities = {getattr(e, "type_", ""): e for e in getattr(document, "entities", [])}
    items = [
        {
            "text": getattr(item, "mention_text", ""),
            "confidence": float(getattr(item, "confidence", 0.0) or 0.0),
        }
        for item in getattr(document, "entities", [])
        if getattr(item, "type_", "") == "item"
    ]
    return {
        "merchant": getattr(entities.get("merchant"), "mention_text", ""),
        "tax": getattr(entities.get("tax"), "mention_text", ""),
        "total": getattr(entities.get("total_amount"), "mention_text", ""),
        "items": items,
        "provider": "google-cloud-documentai",
    }
