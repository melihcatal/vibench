import google.generativeai as genai
import os

def summarize_invoice_fields(invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Google's Generative AI.

    Args:
        invoice_data: A dictionary containing extracted invoice fields.

    Returns:
        A string containing the summary of the invoice fields.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID

    prompt = f"""
    Please summarize the following invoice data in a concise manner:

    Vendor: {invoice_data.get("vendor", "N/A")}
    Date: {invoice_data.get("date", "N/A")}
    Total: {invoice_data.get("total", "N/A")}
    Line Items: {invoice_data.get("line_items", "N/A")}
    """

    response = model.generate_content(prompt)
    return response.text

