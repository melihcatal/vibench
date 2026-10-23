def summarize_invoice_fields(invoice_fields):
    summary = {
        'vendor': invoice_fields.get('Vendor', ''),
        'date': invoice_fields.get('Date', ''),
        'total': invoice_fields.get('Total', '')
    }
    return summary