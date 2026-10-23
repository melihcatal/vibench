# Summarize extracted invoice fields for downstream business logic

import json
from document_models import ExpenseRecord


def summarize_invoice(expense: ExpenseRecord) -> dict:
    """
    Generate a concise summary dictionary from a normalized invoice record.
    The summary includes provider metadata, key line items, and totals.
    """
    summary = {
        "provider": "azure" if expense.get("vendor") else "default",
        "document_type": "invoice",
        "reference_number": expense.get("vendor", "N/A"),
        "date": expense.get("date"),
        "total_amount": expense.get("total"),
        "currency": "USD",  # Assume USD for demo; replace with actual if known
        "line_items": expense.get("items", [])[:5],  # Show first 5 items as preview
    }
    return summary
