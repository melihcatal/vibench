def summarize_invoice_fields(invoice):
    summary = {
        "vendor": invoice.get("vendor"),
        "date": invoice.get("date"),
        "total": invoice.get("total"),
    }
    return summary