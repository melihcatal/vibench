def summarize_invoice_fields(invoice):
    summary = {
        "vendor": invoice.get("vendor"),
        "date": invoice.get("date"),
        "total": invoice.get("total"),
        "item_count": len(invoice.get("line_items", []))
    }
    return summary