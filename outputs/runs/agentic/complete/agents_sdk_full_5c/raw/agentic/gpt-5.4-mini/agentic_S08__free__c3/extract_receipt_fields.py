from typing import Any, Dict

from document_client import load_documentai_client


RECEIPT_PROVIDER = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def extract_receipt_fields(content: bytes) -> Dict[str, Any]:
    client = load_documentai_client()
    doc = client.process_document(content, mime_type="application/pdf")
    entities = doc.get("entities", [])
    items = []
    for entity in entities:
        if entity.get("type_", "").lower() == "line_item":
            items.append(entity.get("mention_text"))
    return {
        "merchant": next((e.get("mention_text") for e in entities if e.get("type_") in {"merchant_name", "supplier_name"}), None),
        "tax": next((e.get("mention_text") for e in entities if e.get("type_") == "total_tax"), None),
        "total": next((e.get("mention_text") for e in entities if e.get("type_") in {"total_amount", "receipt_total"}), None),
        "items": items,
        "provider": RECEIPT_PROVIDER,
    }
