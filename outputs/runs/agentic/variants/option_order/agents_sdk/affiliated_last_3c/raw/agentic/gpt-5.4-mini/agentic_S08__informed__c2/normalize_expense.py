from __future__ import annotations

from typing import Any, Dict, Iterable

from document_models import ExpenseNormalizationResult, StructuredDocumentResponse, coerce_float, normalize_currency


def _to_line_items(items: Any) -> list[dict[str, Any]]:
    normalized = []
    if isinstance(items, Iterable) and not isinstance(items, (str, bytes, dict)):
        for item in items:
            if isinstance(item, dict):
                normalized.append(item)
            else:
                normalized.append({"description": str(item)})
    return normalized


def normalize_expense(extracted: StructuredDocumentResponse) -> Dict[str, Any]:
    values = {field.name: field.value for field in extracted.fields}
    vendor = str(values.get("VendorName") or values.get("MerchantName") or "").strip()
    transaction_date = str(values.get("InvoiceDate") or values.get("Date") or "").strip()
    total_amount = coerce_float(values.get("InvoiceTotal") or values.get("Total"), 0.0)
    currency = normalize_currency(values.get("Currency"))
    line_items = _to_line_items(values.get("Items") or [])
    normalized = ExpenseNormalizationResult(
        vendor=vendor,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
    )
    return {
        "vendor": normalized.vendor,
        "transaction_date": normalized.transaction_date,
        "total_amount": normalized.total_amount,
        "currency": normalized.currency,
        "line_items": normalized.line_items,
        "source_provider": normalized.source_provider,
    }
