def summarize_invoice(invoice):
    summary = {
        "vendor": invoice.get('vendor', ''),
        "date": invoice.get('date', ''),
        "total": invoice.get('total', 0.0),
        "line_items_count": len(invoice.get('line_items', []))
    }
    return summary