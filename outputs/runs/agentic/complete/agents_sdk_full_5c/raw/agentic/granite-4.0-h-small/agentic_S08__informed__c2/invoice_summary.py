from typing import Dict, Any
from document_models import Expense

def summarize_invoice(raw_out: Dict[str, Any]) -> Dict[str, Any]:
    # Convert raw extraction to normalized model
    normalized = normalize_expense(raw_out)
    expense = Expense(**normalized)
    summary = {
        "vendor": expense.vendor,
        "date": expense.date.isoformat() if expense.date else None,
        "total": expense.total,
        "currency": expense.currency,
        "item_count": len(expense.items),
        "items": [{"desc": it.description, "amount": it.total} for it in expense.items]
    }
    return summary
