from extract_invoice_fields import extract_invoice_fields

def summarize_invoice(document_path):
    invoice_fields = extract_invoice_fields(document_path)
    summary = {
        "vendor": invoice_fields.get("vendor"),
        "date": invoice_fields.get("date"),
        "total": invoice_fields.get("total"),
        "item_count": len(invoice_fields.get("line_items", []))
    }
    return summary