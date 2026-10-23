from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import get_document_analysis_client, get_model_id, load_document_bytes, field_value
from document_models import DocumentExtractionResult, ExtractedField, LineItem



def extract_invoice_fields(
    file_path: Optional[str] = None,
    content_base64: Optional[str] = None,
    model_id: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_document_analysis_client()
    payload = load_document_bytes(path=file_path, content_base64=content_base64)
    selected_model = model_id or get_model_id("prebuilt-invoice")
    poller = client.begin_analyze_document(selected_model, document=payload)
    result = poller.result()

    if not result.documents:
        extracted = DocumentExtractionResult(document_type="invoice", provider="azure-ai-formrecognizer")
        return extracted.to_dict()

    doc = result.documents[0]
    vendor_data = field_value(doc, "VendorName")
    date_data = field_value(doc, "InvoiceDate")
    total_data = field_value(doc, "InvoiceTotal")
    currency_data = field_value(doc, "InvoiceTotal")
    notes_data = field_value(doc, "CustomerAddressRecipient", attribute="content")

    items: List[LineItem] = []
    line_items_field = doc.fields.get("Items") if getattr(doc, "fields", None) else None
    if line_items_field and getattr(line_items_field, "value", None):
        for entry in line_items_field.value:
            item_map = getattr(entry, "value", {}) or {}
            desc = item_map.get("Description")
            qty = item_map.get("Quantity")
            unit_price = item_map.get("UnitPrice")
            amount = item_map.get("Amount")
            items.append(
                LineItem(
                    description=getattr(desc, "content", None) or getattr(desc, "value", None) or "",
                    quantity=getattr(qty, "value", None),
                    unit_price=getattr(unit_price, "value", None),
                    total=getattr(amount, "value", None),
                    confidence=min(
                        float(getattr(desc, "confidence", 0.0) or 0.0),
                        float(getattr(amount, "confidence", 0.0) or 0.0) if amount else 0.0,
                    ),
                )
            )

    extracted = DocumentExtractionResult(
        document_type="invoice",
        provider="azure-ai-formrecognizer",
        vendor=ExtractedField(**vendor_data),
        date=ExtractedField(value=str(date_data["value"]) if date_data["value"] is not None else None, confidence=date_data["confidence"]),
        total=ExtractedField(**total_data),
        currency=ExtractedField(value=getattr(currency_data["value"], "currency_code", None), confidence=currency_data["confidence"]),
        notes=ExtractedField(**notes_data),
        line_items=items,
        raw_response={"model_id": selected_model, "api_version": getattr(result, "api_version", None)},
    )
    return extracted.to_dict()
