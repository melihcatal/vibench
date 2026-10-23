def summarize_invoice_fields(invoice_fields):
    summary = {
        "vendor": invoice_fields["vendor"],
        "date": invoice_fields["date"],
        "total": invoice_fields["total"],
        "line_items": invoice_fields["line_items"],
    }
    return summary
