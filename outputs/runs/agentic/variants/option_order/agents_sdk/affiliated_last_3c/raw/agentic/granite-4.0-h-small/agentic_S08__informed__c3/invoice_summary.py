def summarize_invoice(extracted):
    '''Create a concise textual summary of an invoice.
    Uses extracted dict from same-scenario extraction step.
    '''
    vendor = extracted.get('vendor') or 'Unknown Vendor'
    date = extracted.get('date') or 'No date'
    amount = extracted.get('total')
    line_items = extracted.get('line_items')
    items_text = ', '.join(line_items) if line_items else 'No items'
    return f"Invoice from {vendor} dated {date} totaling ${amount:.2f}.\nItems: {items_text}"