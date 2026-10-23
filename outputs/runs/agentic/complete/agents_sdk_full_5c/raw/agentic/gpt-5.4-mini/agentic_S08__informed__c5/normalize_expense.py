from __future__ import annotations

from typing import Any, Dict, Iterable

from document_models import NormalizedExpenseRecord, normalize_money


def _items_from_payload(items: Iterable[Dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for item in items or []:
        normalized.append(
            {
                "description": item.get("description") or item.get("name") or "",
                "quantity": normalize_money(item.get("quantity")),
                "unit_price": normalize_money(item.get("unitPrice") or item.get("unit_price")),
                "amount": normalize_money(item.get("amount") or item.get("total")),
                "confidence": normalize_money(item.get("confidence")),
            }
        )
    return normalized


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    raw = extracted.get("raw", extracted)
    document_type = extracted.get("document_type") or raw.get("documentType") or "expense"
    record = NormalizedExpenseRecord(
        provider=extracted.get("provider", "azure-document-intelligence"),
        document_type=document_type,
        vendor=extracted.get("vendor") or raw.get("vendorName") or raw.get("merchantName") or "",
        date=extracted.get("date") or raw.get("transactionDate") or raw.get("invoiceDate") or "",
        currency=extracted.get("currency") or raw.get("currencyCode") or "",
        subtotal=normalize_money(extracted.get("subtotal") or raw.get("subTotal")),
        tax=normalize_money(extracted.get("tax") or raw.get("totalTax") or raw.get("taxAmount")),
        total=normalize_money(extracted.get("total") or raw.get("total")),
        items=_items_from_payload(extracted.get("items") or raw.get("items") or []),
        notes=extracted.get("notes") or raw.get("memo") or raw.get("note"),
        confidence=extracted.get("confidence") or {},
    )
    return record.__dict__
