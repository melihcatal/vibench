from __future__ import annotations

from typing import Any, Dict, List

from document_models import LineItem, NormalizedExpense, normalize_amount, normalize_date


def normalize_expense(fields: Dict[str, Any]) -> Dict[str, Any]:
    line_items: List[LineItem] = []
    for item in fields.get("line_items", []) or []:
        if isinstance(item, dict):
            line_items.append(
                LineItem(
                    description=str(item.get("description", "")),
                    quantity=normalize_amount(item.get("quantity")),
                    unit_price=normalize_amount(item.get("unit_price")),
                    amount=normalize_amount(item.get("amount")),
                )
            )
    expense = NormalizedExpense(
        vendor=str(fields.get("vendor", "")).strip(),
        transaction_date=normalize_date(fields.get("date") or fields.get("transaction_date")),
        total=normalize_amount(fields.get("total")),
        currency=str(fields.get("currency", "USD")),
        line_items=line_items,
        tax=normalize_amount(fields.get("tax")),
        notes=fields.get("notes"),
    )
    return {
        "vendor": expense.vendor,
        "transaction_date": expense.transaction_date,
        "total": expense.total,
        "currency": expense.currency,
        "line_items": [item.__dict__ for item in expense.line_items],
        "tax": expense.tax,
        "notes": expense.notes,
    }
