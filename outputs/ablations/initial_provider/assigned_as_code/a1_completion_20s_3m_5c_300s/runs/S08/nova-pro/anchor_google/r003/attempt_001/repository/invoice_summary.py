from google.cloud import documentai


def invoice_summary(invoice):
    summary = {
        "vendor": invoice.get("vendor"),
        "date": invoice.get("date"),
        "total": invoice.get("total"),
        "items": [item.get("description") for item in invoice.get("items", [])]
    }
    return summary