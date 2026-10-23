import json
from document_models import NormalizedExpense

def invoice_summary(expense: NormalizedExpense) -> dict:
    """Generate a concise natural-language summary of an invoice expense record."""
    items_desc = ", ".join(item['description'] for item in expense.lineItems[:5])
    if len(expense.lineItems) > 5:
        items_desc += f" and {len(expense.lineItems) - 5} more"
    summary = {
        "expenseId": expense.expenseId,
        "summary": f"Invoice from {expense.vendor} dated {expense.date} totaling ${expense.totalAmount:.2f}. Items include: {items_desc}."
    }
    return summary
