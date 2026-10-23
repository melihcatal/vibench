import os
import google.generativeai as genai

def summarize_invoice_fields(extracted_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Gemini API.
    """
    # Configure the Gemini API client
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Choose a model
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text summarization

    # Construct the prompt for summarization
    prompt = f"""Summarize the following invoice details in a concise paragraph, highlighting the vendor, total amount, and key line items:

Vendor: {extracted_fields.get('vendor_name', 'N/A')}
Date: {extracted_fields.get('transaction_date', 'N/A')}
Total Amount: {extracted_fields.get('total_amount', 'N/A')}
Line Items: {', '.join([f'{item.get("description", "")}: {item.get("amount", "N/A")}' for item in extracted_fields.get('line_items', [])]) if extracted_fields.get('line_items') else 'N/A'}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing invoice: {e}")
        return """
Could not generate summary due to an error.
"""

if __name__ == '__main__':
    # Example Usage
    sample_invoice_fields = {
        "document_type": "invoice",
        "vendor_name": "Example Corp",
        "transaction_date": "2023-10-27",
        "total_amount": "250.75",
        "currency": "USD",
        "line_items": [
            {"description": "Consulting Services", "amount": "200.00"},
            {"description": "Software License", "amount": "50.75"}
        ],
        "tax_amount": "10.00",
        "notes": "Project A Phase 1 services."
    }

    if os.getenv("GOOGLE_API_KEY"):
        print("Generating invoice summary...")
        summary = summarize_invoice_fields(sample_invoice_fields)
        print("Invoice Summary:")
        print(summary)
    else:
        print("Please set the GOOGLE_API_KEY environment variable to use the Gemini API.")
