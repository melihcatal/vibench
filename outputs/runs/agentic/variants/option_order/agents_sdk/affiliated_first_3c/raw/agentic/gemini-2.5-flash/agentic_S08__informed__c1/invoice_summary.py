import os
import google.generativeai as genai
from typing import Dict, Any

def summarize_invoice_fields(invoice_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    """
    # Configure the Gemini API client
    # Ensure GOOGLE_API_KEY environment variable is set
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # Use a specific model that is good for text generation/summarization
    # gemini-pro is a good general-purpose model
    model = genai.GenerativeModel('gemini-pro')

    # Construct a prompt for summarization
    prompt = f"""Summarize the following invoice information. Highlight the vendor, total amount, and key line items.

    Vendor: {invoice_data.get("vendor_name", "N/A")}
    Date: {invoice_data.get("transaction_date", "N/A")}
    Total Amount: {invoice_data.get("total_amount", "N/A")} {invoice_data.get("currency", "")}
    Line Items:
"""
    if invoice_data.get("line_items"):
        for item in invoice_data["line_items"]:
            prompt += f"- {item.get("description", "N/A")}: {item.get("total", "N/A")}\n"
    else:
        prompt += "No line items found.\n"
    
    prompt += "\nProvide a concise summary in a few sentences."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return "Could not generate summary."

if __name__ == "__main__":
    # Example normalized invoice data
    example_invoice = {
        "document_type": "invoice",
        "vendor_name": "Global Widgets Inc.",
        "transaction_date": "2023-10-27T10:30:00",
        "total_amount": 549.99,
        "currency": "USD",
        "tax_amount": 35.00,
        "line_items": [
            {"description": "Premium Widget", "quantity": 2, "unit_price": 200.00, "total": 400.00},
            {"description": "Shipping", "quantity": 1, "unit_price": 114.99, "total": 114.99},
            {"description": "Tax", "quantity": 1, "unit_price": 35.00, "total": 35.00}
        ],
        "raw_extraction": {} 
    }

    # To run this example, set your GOOGLE_API_KEY environment variable.
    # summary = summarize_invoice_fields(example_invoice)
    # print("Invoice Summary:")
    # print(summary)
