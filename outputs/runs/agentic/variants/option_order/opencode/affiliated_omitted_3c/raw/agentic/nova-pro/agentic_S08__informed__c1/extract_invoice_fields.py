import mindee


def extract_invoice_fields(invoice_image_path):
    client = mindee.Client(api_key=os.getenv("MINDEE_API_KEY"))
    invoice_document = client.invoices.parse(invoice_image_path)
    vendor = invoice_document.vendor
    date = invoice_document.date
    total = invoice_document.total
    line_items = invoice_document.line_items
    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}
