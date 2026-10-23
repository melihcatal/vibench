# [LATER-STEP] invoice_summary.py
# Summarize extracted invoice fields

from typing import List, TypedDict
from document_models import NormalizedExpense


# Example summarization function that aggregates line items into a concise report
class InvoiceSummary(TypedDict):
    vendor: str
    date: str
    total: float
    tax: float
    items_summary: str  # e.g. "5 items totaling $123.45"


def summarize_invoice(expense: NormalizedExpense) -> InvoiceSummary:
    item_count = len(expense["items"])
    items_str = f"{item_count} items totaling ${expense['total']:.2f}"
    return {
        "vendor": expense["vendor"],
        "date": expense["date"],
        "total": expense["total"],
        "tax": expense["tax"],
        "items_summary": items_str,
    }
