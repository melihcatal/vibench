import json

def summarize_invoice_fields(invoice_data):
    summary = {
        "vendor": invoice_data["vendor"],
        "date": invoice_data["date"],
        "total": invoice_data["total"],
        "line_items_count": len(invoice_data["line_items"])
    }
    return json.dumps(summary, indent=2)