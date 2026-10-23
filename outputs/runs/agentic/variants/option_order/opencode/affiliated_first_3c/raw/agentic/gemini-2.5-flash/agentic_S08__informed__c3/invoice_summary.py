import os
import json
import google.generativeai as genai


def summarize_invoice_fields(extracted_invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    invoice_data_str = json.dumps(extracted_invoice_data, indent=2)

    prompt = f"""Summarize the key information from the following extracted invoice data in a concise paragraph. 
    Highlight the vendor, total amount, and any key line items if present.

Extracted Invoice Data:
{invoice_data_str}

Summary:"""

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation
    response = model.generate_content(prompt)

    return response.text.strip()


if __name__ == "__main__":
    # Example usage - replace with actual data
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    if not google_api_key:
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        dummy_invoice_data = {
            "vendor_name": "Global Supplies Inc.",
            "invoice_date": "2023-10-25",
            "total_amount": "750.50 USD",
            "line_items": [
                {"description": "Office Chairs", "amount": "300.00"},
                {"description": "Desk Lamps", "amount": "250.00"},
                {"description": "Shipping", "amount": "25.50"},
            ],
            "invoice_number": "INV-2023-001",
            "currency": "USD",
        }

        print(f"Summarizing invoice fields using Google Gemini API...")
        # summary = summarize_invoice_fields(dummy_invoice_data)
        # print(f"Invoice Summary: {summary}")
