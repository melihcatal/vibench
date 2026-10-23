# [LATER-STEP] invoice_summary.py
from normalize_expense import NormalizedExpense
from typing import Literal

def summarize_invoice(expense: NormalizedExpense) -> dict:
    """Generate a concise summary of an invoice expense record.

    Returns a JSON‑serializable dict containing key fields.
    """
    if expense.source_type != 'invoice':
        raise ValueError('Only invoices can be summarized')
    return {
        'vendor': expense.vendor,
        'date': expense.date,
        'total_amount': expense.amount,
        'currency_hint': 'USD',  # placeholder; map to locale if available
        'line_items': expense.line_items
    }