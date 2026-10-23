import json
from document_models import NormalizedExpense


def summarize_invoice(expense: NormalizedExpense) -> str:
    """
    Create a concise summary string for an invoice expense record.
    Includes vendor, total, and a bulleted list of line items.
    """
    summary = f"Invoice from {expense['vendor']} totaling ${expense['total']}\n"
    items = expense.get("line_items", [])
    if items:
        summary += "Line items:\\n"
        for it in items:
            summary += f"- {it['description']}: ${it['amount']}\\n"
    else:
        summary += "No line items found.\n"
    return summary
