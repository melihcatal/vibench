from __future__ import annotations

from typing import Any, Dict, List

from document_client import get_document_analysis_client
from document_models import ExtractedDocument, LineItem, parse_float


AZURE_MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(document_bytes: bytes) -> Dict[str, Any]:
    client = get_document_analysis_client()
    poller = client.begin_analyze_document(AZURE_MODEL_ID, document=document_bytes)
    result = poller.result()

    if not result.documents:
        return ExtractedDocument(document_type="invoice", raw_response={"documents": []}).__dict__

    doc = result.documents[0]
    fields = doc.fields or {}

    vendor_name = fields.get("VendorName")
    invoice_date = fields.get("InvoiceDate")
    invoice_total = fields.get("InvoiceTotal")
    items_field = fields.get("Items")

    items: List[LineItem] = []
    if items_field and items_field.value:
        for item in items_field.value:
            item_fields = item.value or {}
            items.append(
                LineItem(
                    description=(item_fields.get("Description").value if item_fields.get("Description") else ""),
                    quantity=parse_float(item_fields.get("Quantity").value if item_fields.get("Quantity") else None),
                    unit_price=parse_float(item_fields.get("UnitPrice").value if item_fields.get("UnitPrice") else None),
                    amount=parse_float(item_fields.get("Amount").value if item_fields.get("Amount") else None),
                    confidence=min(
                        [
                            x.confidence
                            for x in item_fields.values()
                            if getattr(x, "confidence", None) is not None
                        ]
                        or [None]
                    ),
                )
            )

    extracted = ExtractedDocument(
        document_type="invoice",
        vendor=vendor_name.value if vendor_name else None,
        invoice_date=str(invoice_date.value) if invoice_date and invoice_date.value is not None else None,
        total=parse_float(invoice_total.value if invoice_total else None),
        currency=(invoice_total.value.currency_code if invoice_total and getattr(invoice_total.value, "currency_code", None) else None),
        items=items,
        raw_response={
            "model_id": AZURE_MODEL_ID,
            "doc_type": doc.doc_type,
            "confidence": doc.confidence,
        },
    )
    return {
        **extracted.__dict__,
        "items": [item.__dict__ for item in extracted.items],
    }
