import os
from mindee import Client, product


def extract_invoice_fields(file_path: str):
    """
    Extracts structured fields from an invoice document using Mindee API.
    """
    api_key = os.environ.get("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set.")

    mindee_client = Client(api_key=api_key)

    with open(file_path, "rb") as f:
        input_doc = mindee_client.source_from_file(f)

    result = mindee_client.parse(product.InvoiceV4, input_doc)

    if result.document:
        return result.document.inference.prediction.fields
    return None
