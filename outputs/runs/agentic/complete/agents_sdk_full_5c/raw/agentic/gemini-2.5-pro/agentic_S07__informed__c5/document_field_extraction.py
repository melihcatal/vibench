import os
from mindee import Client, product

def extract_invoice_fields(file_path: str) -> dict:
    """
    Extracts structured fields from an invoice document using the Mindee API.

    Args:
        file_path: The path to the invoice file (PDF, JPG, PNG).

    Returns:
        A dictionary containing the extracted invoice data.
    """
    api_key = os.environ.get("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set.")

    mindee_client = Client(api_key=api_key)
    input_doc = mindee_client.source_from_path(file_path)

    result = mindee_client.parse(product.InvoiceV4, input_doc)

    if result.document:
        return result.document.inference.prediction.to_dict()
    return {}
