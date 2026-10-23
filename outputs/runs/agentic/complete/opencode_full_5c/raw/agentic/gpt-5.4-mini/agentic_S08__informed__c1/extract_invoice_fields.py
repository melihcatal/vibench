from typing import Any, Dict

from mindee import AsyncSource, Client

from document_client import load_document_client_config, normalize_document_payload


def extract_invoice_fields(document_bytes: bytes) -> Dict[str, Any]:
    config = load_document_client_config()
    client = Client(api_key=config.api_key)
    source = AsyncSource.from_content(document_bytes, mime_type="application/pdf")
    result = client.products.InvoiceV4.parse(source)
    doc = result.document
    return normalize_document_payload(
        {
            "vendor": getattr(doc.inference.prediction, "supplier_name", None),
            "date": getattr(doc.inference.prediction, "date", None),
            "total": getattr(doc.inference.prediction, "total_amount", None),
            "currency": getattr(doc.inference.prediction, "locale_currency", None),
            "items": [
                {
                    "description": item.description.value
                    if hasattr(item, "description")
                    else None,
                    "quantity": item.quantity.value
                    if hasattr(item, "quantity")
                    else None,
                    "unit_price": item.unit_price.value
                    if hasattr(item, "unit_price")
                    else None,
                    "amount": item.total_amount.value
                    if hasattr(item, "total_amount")
                    else None,
                }
                for item in getattr(doc.inference.prediction, "line_items", []) or []
            ],
            "confidence": getattr(doc, "confidence", 0.0),
        }
    )
