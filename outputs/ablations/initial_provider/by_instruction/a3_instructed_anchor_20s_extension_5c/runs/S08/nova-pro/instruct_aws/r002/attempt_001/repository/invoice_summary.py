def summarize_invoice_fields(extracted_fields):
    summary = {
        'vendor': extracted_fields.get('Vendor', ''),
        'date': extracted_fields.get('Date', ''),
        'total': extracted_fields.get('Total', '')
    }
    return summary