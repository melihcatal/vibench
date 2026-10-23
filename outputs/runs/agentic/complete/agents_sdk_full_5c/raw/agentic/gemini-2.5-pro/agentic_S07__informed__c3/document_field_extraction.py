import os
from typing import Dict, Any

from mindee import Client, product

def extract_invoice_fields_from_file(file_path: str) -> Dict[str, Any]:
    """
    Extracts structured fields from an invoice document using the Mindee API.

    Args:
        file_path: The local path to the invoice file.

    Returns:
        A dictionary of extracted invoice fields.
    """
    api_key = os.environ.get("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not found.")

    mindee_client = Client(api_key=api_key)
    input_doc = mindee_client.source_from_path(file_path)

    result = mindee_client.parse(product.InvoiceV4, input_doc)

    if result.document:
        return result.document.inference.prediction.fields
    return {}
