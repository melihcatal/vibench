# invoice_summary.py
# Summarize extracted invoice fields for downstream use
from typing import TypedDict

# Reuse the normalized schema defined in document_models.py
from document_models import ExpenseResponse

# Example summary builder - in a real workflow this would be a separate microservice or function
def summarize_invoice(expense: ExpenseResponse) -> dict:
    """Create a concise summary dict from a normalized expense record.",
    summary = {
        "merchant_or_vendor": expense.get('vendor_or_merchant'),
        "transaction_date": expense.get('date'),
        "total_amount": expense.get('total'),
        "currency": expense.get('currency'),
        "line_item_count": len(expense.get('line_items', []))
    }
    return summary
