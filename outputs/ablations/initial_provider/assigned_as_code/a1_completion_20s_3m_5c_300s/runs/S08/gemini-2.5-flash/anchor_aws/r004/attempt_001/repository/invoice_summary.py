import os
from typing import Dict, Any
from document_models import InvoiceFields
import google.generativeai as genai

def summarize_invoice_fields(invoice_fields: InvoiceFields) -> Dict[str, Any]:
    # Configure the Generative AI client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    summary_prompt = f"""Summarize the following invoice details in a concise paragraph:
    Vendor: {invoice_fields.vendor}
    Date: {invoice_fields.date}
    Total: {invoice_fields.total}
    Line Items: {', '.join([f'{item.description} (Qty: {item.quantity}, Amt: {item.amount})' for item in invoice_fields.line_items])}
    """

    try:
        response = model.generate_content(summary_prompt)
        summary_text = response.text
    except Exception as e:
        summary_text = f"Failed to generate summary: {e}"

    return {"invoice_summary": summary_text}
