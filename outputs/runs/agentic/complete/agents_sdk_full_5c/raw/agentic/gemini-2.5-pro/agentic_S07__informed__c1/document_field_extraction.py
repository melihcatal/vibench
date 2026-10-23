import os
from mindee import Client, product

def extract_invoice_fields(file_path: str) -> dict:
    """
    Extracts structured fields from an invoice document using the Mindee API.

    Args:
        file_path: The local path to the invoice file (PDF, JPG, PNG).

    Returns:
        A dictionary of extracted invoice fields.
    """
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set.")

    mindee_client = Client(api_key=api_key)

    try:
        input_doc = mindee_client.source_from_path(file_path)
        
        # Use the InvoiceV4 model from Mindee
        result = mindee_client.parse(
            product.InvoiceV4,
            input_doc
        )

        if result.document:
            return result.document.inference.prediction.to_dict()
        else:
            return {"error": "Failed to parse document."}
            
    except Exception as e:
        return {"error": str(e)}
