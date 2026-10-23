import json


def summarize_invoice(invoice):
    summary = {
        "vendor": invoice.get("vendor"),
        "date": invoice.get("date"),
        "total": invoice.get("total"),
        "item_count": len(invoice.get("items", []))
    }
    return json.dumps(summary, default=str)