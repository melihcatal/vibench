def summarize_invoice(data: dict) -> str:
    vendor = data.get('vendor') or data.get('merchant')
    date = data.get('date')
    total = data.get('total')
    items = data.get('line_items')
    summary = f"Vendor: {vendor or 'N/A'}\nDate: {date or 'N/A'}\nTotal: {total or 'N/A'}\n"
    if items:
        summary += "Line Items:\n"
        for item in items:
            summary += f"  - {item.get('description') or item.get('name')}: {item.get('quantity') or 1} x {item.get('amount') or item.get('price') or 'N/A'}\n"
    else:
        summary += "No line items found.\n"
    return summary
