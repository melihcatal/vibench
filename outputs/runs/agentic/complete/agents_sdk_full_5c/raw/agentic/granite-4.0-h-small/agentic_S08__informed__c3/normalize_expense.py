from dataclasses import asdict
from typing import List, Dict
from document_models import ExpenseRecord, NormalizedExpense, LineItem

def normalize_expense(expense: ExpenseRecord) -> NormalizedExpense:
    # Map fields to a standard JSON schema
    normalized = {
        "vendor": expense.vendor or "UNKNOWN_VENDOR",
        "date": expense.date or "",
        "total": expense.total or 0.0,
        "currency": expense.currency or "USD",
        "line_items": []
    }
    # Populate line items if available; otherwise infer from receipt data if present
    if expense.line_items:
        for item in expense.line_items:
            normalized["line_items"].append(
                {
                    "description": item.description or "",
                    "quantity": item.quantity or 1,
                    "unit_price": item.unit_price or 0.0,
                    "total": item.total or 0.0,
                    "tax": item.tax or 0.0
                }
            )
    else:
        # Fallback: flatten receipt items
        for item in expense.raw_data.get("line_items", []):
            normalized["line_items"].append(
                {
                    "description": item.get("description", ""),
                    "quantity": item.get("quantity", 1),
                    "unit_price": item.get("unit_price", 0.0),
                    "total": item.get("total", 0.0),
                    "tax": item.get("tax", 0.0)
                }
            )
    return NormalizedExpense(**normalized)
