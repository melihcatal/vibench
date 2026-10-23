import os
from google.cloud import aiplatform
import google.generativeai as genai

def summarize_invoice_fields(invoice_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud's Generative AI.

    Args:
        invoice_fields: A dictionary of extracted invoice fields (e.g., {"total_amount": "100.00", "vendor_name": "Example Corp"}).

    Returns:
        A string containing the summary of the invoice fields.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    # For local development, you might set it like:
    # export GOOGLE_API_KEY="YOUR_API_KEY"
    # Or in a production environment, use service account authentication.
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."

    model = genai.GenerativeModel('gemini-pro')

    prompt = "Summarize the following invoice details:
"
    for key, value in invoice_fields.items():
        prompt += f"- {key.replace('_', ' ').title()}: {value}
"
    prompt += "Provide a concise summary."

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage:
    sample_invoice_fields = {
        "vendor_name": "ABC Supplies Inc.",
        "invoice_number": "INV-2023-001",
        "invoice_date": "2023-10-26",
        "total_amount": "150.75",
        "currency": "USD",
        "items": [
            {"description": "Product A", "quantity": "2", "unit_price": "25.00"},
            {"description": "Product B", "quantity": "1", "unit_price": "100.00"}
        ]
    }
    summary = summarize_invoice_fields(sample_invoice_fields)
    print("Invoice Summary:")
    print(summary)
