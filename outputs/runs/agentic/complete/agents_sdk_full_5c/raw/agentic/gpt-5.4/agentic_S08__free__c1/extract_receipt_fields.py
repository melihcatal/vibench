from __future__ import annotations

from typing import Any, Dict, List

from document_client import get_document_analysis_client
from document_models import ExtractedDocument, LineItem, parse_float


AZURE_MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    client = get_document_analysis_client()
    poller = client.begin_analyze_document(AZURE_MODEL_ID, document=document_bytes)
    result = poller.result()

    if not result.documents:
        return ExtractedDocument(document_type="receipt", raw_response={"documents": []}).__dict__

    doc = result.documents[0]
    fields = doc.fields or {}

    merchant = fields.get("MerchantName")
    tax = fields.get("TotalTax")
    total = fields.get("Total")
    items_field = fields.get("Items")

    items: List[LineItem] = []
    if items_field and items_field.value:
        for item in items_field.value:
            item_fields = item.value or {}
            items.append(
                LineItem(
                    description=(item_fields.get("Description").value if item_fields.get("Description") else ""),
                    quantity=parse_float(item_fields.get("Quantity").value if item_fields.get("Quantity") else None),
                    unit_price=parse_float(item_fields.get("Price").value if item_fields.get("Price") else None),
                    amount=parse_float(item_fields.get("TotalPrice").value if item_fields.get("TotalPrice") else None),
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
        document_type="receipt",
        merchant=merchant.value if merchant else None,
        tax=parse_float(tax.value if tax else None),
        total=parse_float(total.value if total else None),
        currency=(total.value.currency_code if total and getattr(total.value, "currency_code", None) else None),
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
