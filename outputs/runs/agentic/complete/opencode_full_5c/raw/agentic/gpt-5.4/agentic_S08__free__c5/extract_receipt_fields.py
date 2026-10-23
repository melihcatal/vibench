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


def _extract_receipt_items(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = []
    for entry in (doc.get("fields", {}).get("Items") or {}).get("valueArray", []):
        values = entry.get("valueObject", {})
        items.append(
            {
                "description": _extract_field_value(values.get("Description"))
                or _extract_field_value(values.get("Name")),
                "quantity": _extract_field_value(values.get("Quantity")),
                "unit_price": _extract_field_value(values.get("Price")),
                "amount": _extract_field_value(values.get("TotalPrice")),
                "confidence": values.get("TotalPrice", {}).get("confidence")
                or values.get("Description", {}).get("confidence")
                or 0.0,
            }
        )
    return items


def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    client = AzureDocumentIntelligenceClient()
    response = client.analyze_document(document_bytes, model_id="prebuilt-receipt")
    documents = response.get("analyzeResult", {}).get("documents", [])
    receipt = documents[0] if documents else {}
    fields = receipt.get("fields", {})
    result = ExtractionResult(
        document_type="receipt",
        merchant=_extract_field_value(fields.get("MerchantName")),
        invoice_date=_extract_field_value(fields.get("TransactionDate")),
        total=_extract_field_value(fields.get("Total")),
        tax=_extract_field_value(fields.get("TotalTax")),
        currency=(fields.get("Total", {}).get("valueCurrency") or {}).get(
            "currencyCode"
        ),
        notes=_extract_field_value(fields.get("MerchantAddress")),
        line_items=[build_line_item(item) for item in _extract_receipt_items(receipt)],
        confidence_scores={
            "merchant": fields.get("MerchantName", {}).get("confidence", 0.0),
            "transaction_date": fields.get("TransactionDate", {}).get(
                "confidence", 0.0
            ),
            "total": fields.get("Total", {}).get("confidence", 0.0),
            "tax": fields.get("TotalTax", {}).get("confidence", 0.0),
            "items": max(
                [
                    item.get("confidence", 0.0)
                    for item in _extract_receipt_items(receipt)
                ]
                or [0.0]
            ),
        },
        raw_response=response,
    )
    return result.to_dict()
