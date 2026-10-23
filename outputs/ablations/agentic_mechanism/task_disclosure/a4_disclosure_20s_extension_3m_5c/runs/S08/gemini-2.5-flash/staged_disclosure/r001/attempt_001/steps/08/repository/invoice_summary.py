import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

def summarize_invoice_fields(invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud's Vertex AI.

    Args:
        invoice_data: A dictionary containing extracted invoice fields.

    Returns:
        A string summarizing the invoice fields.
    """
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))
    model = GenerativeModel("gemini-pro")

    prompt = f"""
    Please summarize the following invoice data in a concise manner:

    {invoice_data}

    Highlight key information such as vendor, total amount, due date, and line items if available.
    """

    response = model.generate_content([prompt])
    return response.text

if __name__ == "__main__":
    # Example usage:
    sample_invoice_data = {
        "vendor_name": "ABC Supplies Inc.",
        "invoice_number": "INV-2023-001",
        "invoice_date": "2023-10-26",
        "due_date": "2023-11-26",
        "total_amount": "150.75 USD",
        "currency": "USD",
        "line_items": [
            {"description": "Product A", "quantity": 2, "unit_price": 25.00, "total": 50.00},
            {"description": "Product B", "quantity": 1, "unit_price": 75.25, "total": 75.25},
            {"description": "Shipping", "quantity": 1, "unit_price": 25.50, "total": 25.50},
        ],
        "tax_amount": "10.00 USD",
        "subtotal": "140.75 USD"
    }

    # Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables are set
    # For example:
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

    if os.getenv("GOOGLE_CLOUD_PROJECT") and os.getenv("GOOGLE_CLOUD_LOCATION"):
        summary = summarize_invoice_fields(sample_invoice_data)
        print("Invoice Summary:")
        print(summary)
    else:
        print("Please set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables.")
        print("Example: export GOOGLE_CLOUD_PROJECT='your-project-id'")
        print("         export GOOGLE_CLOUD_LOCATION='us-central1'")
