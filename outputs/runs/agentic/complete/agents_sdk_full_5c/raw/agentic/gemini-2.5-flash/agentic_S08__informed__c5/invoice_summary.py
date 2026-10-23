import os
import json
import google.generativeai as genai
from document_models import NormalizedExpense

def summarize_invoice_fields(normalized_invoice: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    invoice_data_json = normalized_invoice.to_json()

    prompt = f"""Generate a concise summary of the following invoice data. Highlight key information like vendor, total amount, date, and a brief overview of line items. Keep the summary under 100 words.\n\nInvoice Data:\n{invoice_data_json}"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating invoice summary with Gemini API: {e}")
        return f"Failed to generate summary: {str(e)}. Original total: {normalized_invoice.total_amount if normalized_invoice.total_amount else 'N/A'}"

if __name__ == '__main__':
    # Example usage with a dummy NormalizedExpense object
    sample_invoice_data = NormalizedExpense.from_dict({
        "expense_type": "invoice",
        "date": "2023-10-26",
        "vendor_name": "Global Tech Solutions",
        "total_amount": 1500.75,
        "currency": "USD",
        "tax_amount": 100.25,
        "line_items": [
            {"description": "Software License", "quantity": 1, "unit_price": 1200.00, "total_price": 1200.00},
            {"description": "Support Fee (Annual)", "quantity": 1, "unit_price": 200.50, "total_price": 200.50}
        ],
        "original_extracted_data": {"some_raw_field": "raw_value"}
    })

    if not os.environ.get("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        print("Generating invoice summary...")
        summary = summarize_invoice_fields(sample_invoice_data)
        print("\nInvoice Summary:\n", summary)
