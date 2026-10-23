import os
from mindee import Client


def extract_invoice_fields(invoice_path):
    client = Client(api_key=os.getenv("MINDEE_API_KEY"))
    invoice_document = client.documents.create(invoice_path)
    invoice_document.wait_for_completion()
    return invoice_document.prediction.inference.data
