from typing import Any, Dict

from document_client import load_documentai_client
from document_models import LineItem


DOCUMENT_AI_INVOICE_PROCESSOR_HINT = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def extract_invoice_fields(content: bytes) -> Dict[str, Any]:
    client = load_documentai_client()
    doc = client.process_document(content, mime_type="application/pdf")
    entities = doc.get("entities", [])
    items = []
    for entity in entities:
        if entity.get("type_", "").lower() == "line_item":
            props = {p.get("type_"): p.get("mention_text") for p in entity.get("properties", [])}
            items.append(
                LineItem(
                    description=props.get("description", ""),
                    quantity=float(props.get("quantity", 0) or 0),
                    unit_price=float(props.get("unit_price", 0) or 0),
                    amount=float(props.get("amount", 0) or 0),
                ).__dict__
            )
    return {
        "vendor": next((e.get("mention_text") for e in entities if e.get("type_") == "supplier_name"), None),
        "date": next((e.get("mention_text") for e in entities if e.get("type_") == "invoice_date"), None),
        "total": next((e.get("mention_text") for e in entities if e.get("type_") in {"total_amount", "amount_due"}), None),
        "line_items": items,
        "provider": DOCUMENT_AI_INVOICE_PROCESSOR_HINT,
    }
