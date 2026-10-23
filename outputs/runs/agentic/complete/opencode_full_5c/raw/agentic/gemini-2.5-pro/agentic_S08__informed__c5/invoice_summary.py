import os
import google.generativeai as genai
from document_models import Invoice


def summarize_invoice(invoice: Invoice) -> str:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following invoice:
    
    Vendor: {invoice.vendor_name}
    Date: {invoice.invoice_date}
    Total: {invoice.invoice_total}
    
    Line Items:
    """
    for item in invoice.line_items:
        prompt += f"- {item.description}: {item.total_price}\n"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during summarization: {e}"
