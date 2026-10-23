from mindee import Client, InvoiceDocument


def summarize_invoice_fields(invoice_path):
    client = Client(api_key=os.getenv("MINDEE_API_KEY"))
    document = client.documents.create(invoice_path, type="invoice")
    invoice = document.inference(type="invoice")
    return f"Invoice from {invoice.vendor} on {invoice.date} for a total of {invoice.total} with {len(invoice.line_items)} line items."
