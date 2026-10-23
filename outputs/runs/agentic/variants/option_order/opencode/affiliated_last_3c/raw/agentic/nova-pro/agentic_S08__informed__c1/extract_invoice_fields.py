from mindee import Client, InvoiceDocument


def extract_invoice_fields(invoice_path):
    client = Client(api_key=os.getenv("MINDEE_API_KEY"))
    document = client.documents.create(invoice_path, type="invoice")
    invoice = document.inference(type="invoice")
    return {
        "vendor": invoice.vendor,
        "date": invoice.date,
        "total": invoice.total,
        "line_items": invoice.line_items,
    }
