# [LATER-STEP] invoice_summary.py
# Summarizes extracted invoice fields for reporting

from document_models import InvoiceResponse, normalize_record

SUMMARY_FIELDS = {
    "vendor": "<no vendor>",
    "date": "<no date>",
    "total": 0.0,
    "line_items_count": 0,
}


def summarize(invoice: InvoiceResponse) -> Dict[str, Any]:
    """Create a concise summary from the normalized invoice object."""
    # Start from the canonical schema template
    summary = SUMMARY_FIELDS.copy()
    # Populate from object when available
    summary["vendor"] = invoice.vendor
    summary["date"] = invoice.date
    summary["total"] = invoice.total
    summary["line_items_count"] = len(invoice.line_items)
    return summary


if __name__ == "__main__":
    # Demo using the dummy data from normalize_expense.py
    # Assume we have a normalized record
    dummy_record = {
        "vendor": "Acme Corp",
        "date": "2024-09-01",
        "total": 123.45,
        "line_items": [
            {"description": "Widget", "quantity": 2, "unit_price": 45.0, "total": 90.0},
            {
                "description": "Gadget",
                "quantity": 1,
                "unit_price": 33.45,
                "total": 33.45,
            },
        ],
    }
    normalized = normalize_record(dummy_record)
    # Wrap into our response model for consistency
    invoice = InvoiceResponse(**normalized)
    print("Invoice summary:", summarize(invoice))
