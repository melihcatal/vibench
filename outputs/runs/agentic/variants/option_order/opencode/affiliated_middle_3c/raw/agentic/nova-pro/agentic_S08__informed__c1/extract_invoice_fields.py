from mindee import Client, InvoiceDocument


def extract_invoice_fields(invoice_path):
    api_key = os.getenv("MINDEE_API_KEY")
    client = Client(api_key)
    document = client.doc_from_path(invoice_path)
    invoice = document.predict(InvoiceDocument)
    return {
        "vendor": invoice.vendor,
        "date": invoice.date,
        "total": invoice.total,
        "line_items": invoice.line_items,
    }
