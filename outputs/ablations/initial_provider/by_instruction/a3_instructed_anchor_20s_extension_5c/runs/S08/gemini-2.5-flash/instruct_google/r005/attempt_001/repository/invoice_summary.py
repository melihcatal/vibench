import os
from typing import Optional

import google.generativeai as genai

from document_models import ExtractedInvoiceFields

def summarize_invoice(
    invoice_fields: ExtractedInvoiceFields,
    model_name: str = "gemini-pro",
    api_key: Optional[str] = None,
) -> str:
    """Summarizes extracted invoice fields using Google's Generative AI."""

    api_key = api_key or os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
    if not api_key:
        raise ValueError("Google Generative AI API Key must be provided or set as environment variable GOOGLE_GENERATIVE_AI_API_KEY.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    summary_prompt = (
        f"Summarize the following invoice details:\n"
        f"Vendor: {invoice_fields.vendor_name or 'N/A'}\n"
        f"Date: {invoice_fields.invoice_date or 'N/A'}\n"
        f"Total Amount: {invoice_fields.total_amount or 'N/A'} {invoice_fields.currency or ''}\n"
        f"Line Items: "
    )

    if invoice_fields.line_items:
        for item in invoice_fields.line_items:
            summary_prompt += (
                f"  - {item.description} (Qty: {item.quantity or 'N/A'}, "
                f"Unit Price: {item.unit_price or 'N/A'}, Total: {item.total_price or 'N/A'})\n"
            )
    else:
        summary_prompt += "None\n"

    response = model.generate_content(summary_prompt)

    return response.text
