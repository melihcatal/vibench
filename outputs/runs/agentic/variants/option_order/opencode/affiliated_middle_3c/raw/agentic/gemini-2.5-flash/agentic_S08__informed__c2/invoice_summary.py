import os
import google.generativeai as genai
from document_models import ExtractedInvoice


def summarize_invoice(invoice_data: ExtractedInvoice) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following invoice data:
    Vendor Name: {invoice_data.vendor_name or "N/A"}
    Invoice Date: {invoice_data.invoice_date or "N/A"}
    Invoice Total: {invoice_data.invoice_total or "N/A"}
    Line Items: {", ".join([f"{item.description} (Qty: {item.quantity or 'N/A'}, Price: {item.total_price or 'N/A'})" for item in invoice_data.line_items]) if invoice_data.line_items else "N/A"}

    Provide a concise summary of the invoice, highlighting key information such as vendor, total amount, and a brief overview of the items.
    """

    response = model.generate_content(prompt)
    return response.text
