from google.cloud import documentai


def invoice_summary(invoice):
    summary = f"Invoice from {invoice['vendor']} on {invoice['date']} for a total of {invoice['total']}"
    return summary
