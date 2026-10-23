from typing import TypedDict
from document_models import NormalizedExpense


def generate_invoice_summary(expense: NormalizedExpense) -> str:
    """Create a human‑readable summary of the extracted invoice."""
    items = expense.get("items", [])
    line_items_text = "\n    ".join(
        f"{i['description']} – ${i['price']} x {i['qty']} = ${i['total']}"
        for i in items
    )
    summary = (
        f"Invoice from: {expense['vendor']}\n"
        f"Date: {expense['date']}\n"
        f"Total: ${expense['total']}\n"
        f"Items:\n    {line_items_text}"
    )
    return summary
