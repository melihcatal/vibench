def summarize_invoice_fields(invoice_data):
    return f"Invoice from {invoice_data['vendor']} on {invoice_data['date']} for a total of {invoice_data['total']}"
