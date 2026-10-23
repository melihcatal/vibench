from __future__ import annotations

from typing import Any, Dict, List

from document_client import AzureDocumentIntelligenceClient
from document_models import ExtractionResult, build_line_item


def _extract_field_value(field: Dict[str, Any]) -> Any:
    if not field:
        return None
    for key in ("valueString", "valueDate", "valueCurrency", "valueNumber", "content"):
        value = field.get(key)
        if isinstance(value, dict) and "amount" in value:
            return value.get("amount")
        if value not in (None, ""):
            return value
    return None


def _extract_items(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = []
    for entry in (doc.get("fields", {}).get("Items") or {}).get("valueArray", []):
        values = entry.get("valueObject", {})
        items.append(
            {
                "description": _extract_field_value(values.get("Description")),
                "quantity": _extract_field_value(values.get("Quantity")),
                "unit_price": _extract_field_value(values.get("UnitPrice")),
                "amount": _extract_field_value(values.get("Amount")),
                "confidence": values.get("Amount", {}).get("confidence")
                or values.get("Description", {}).get("confidence")
                or 0.0,
            }
        )
    return items


def extract_invoice_fields(document_bytes: bytes) -> Dict[str, Any]:
    client = AzureDocumentIntelligenceClient()
    response = client.analyze_document(
        document_bytes,
        model_id="prebuilt-invoice",
        features="queryFields",
    )
    documents = response.get("analyzeResult", {}).get("documents", [])
    invoice = documents[0] if documents else {}
    fields = invoice.get("fields", {})
    result = ExtractionResult(
        document_type="invoice",
        vendor=_extract_field_value(fields.get("VendorName")),
        invoice_date=_extract_field_value(fields.get("InvoiceDate")),
        total=_extract_field_value(fields.get("InvoiceTotal")),
        tax=_extract_field_value(fields.get("TotalTax")),
        currency=(fields.get("InvoiceTotal", {}).get("valueCurrency") or {}).get(
            "currencyCode"
        ),
        notes=_extract_field_value(fields.get("CustomerAddressRecipient"))
        or _extract_field_value(fields.get("RemittanceAddressRecipient")),
        line_items=[build_line_item(item) for item in _extract_items(invoice)],
        confidence_scores={
            "vendor": fields.get("VendorName", {}).get("confidence", 0.0),
            "invoice_date": fields.get("InvoiceDate", {}).get("confidence", 0.0),
            "total": fields.get("InvoiceTotal", {}).get("confidence", 0.0),
            "tax": fields.get("TotalTax", {}).get("confidence", 0.0),
            "line_items": max(
                [item.get("confidence", 0.0) for item in _extract_items(invoice)]
                or [0.0]
            ),
        },
        raw_response=response,
    )
    return result.to_dict()
