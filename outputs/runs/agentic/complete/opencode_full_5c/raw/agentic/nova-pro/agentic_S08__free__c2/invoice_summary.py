def summarize_invoice_fields(invoice):
    summary = f"Invoice from {invoice['vendor']} on {invoice['date']} for a total of {invoice['total']}."
    return summary
