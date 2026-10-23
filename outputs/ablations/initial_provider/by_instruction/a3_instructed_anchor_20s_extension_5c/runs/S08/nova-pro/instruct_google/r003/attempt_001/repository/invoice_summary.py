def summarize_invoice_fields(vendor, date, total, items):
    summary = f'Invoice from {vendor} on {date} for a total of {total}. Items: {items}'
    return summary