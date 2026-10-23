import os
import google.generativeai as genai
from typing import Dict, Any
from document_models import ExtractedInvoice


def summarize_invoice_fields(invoice_data: ExtractedInvoice) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro for text summarization

    summary_prompt = f"""Summarize the following invoice details concisely:
    Vendor Name: {invoice_data.vendor_name.value}
    Invoice Date: {invoice_data.invoice_date.value}
    Total Amount: {invoice_data.total_amount.value} {invoice_data.currency.value}
    Line Items: {", ".join([f"{item.description} ({item.total_price})" for item in invoice_data.line_items]) if invoice_data.line_items else "N/A"}
    Notes: {invoice_data.notes.value if invoice_data.notes else "N/A"}

    Provide a brief summary, highlighting key information such as the vendor, total amount, and a general overview of items or purpose.
    """

    response = model.generate_content(summary_prompt)
    return response.text
