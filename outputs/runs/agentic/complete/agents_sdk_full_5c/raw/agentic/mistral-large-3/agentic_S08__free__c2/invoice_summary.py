from typing import Dict, Any
import openai
from document_models import InvoiceFields


def summarize_invoice_fields(invoice_data: InvoiceFields) -> str:
    """Summarize extracted invoice fields using OpenAI's GPT-4."""
    openai.api_key = "sk-proj-..."
    prompt = (
        f"Summarize the following invoice details in a concise paragraph:\n"
        f"Vendor: {invoice_data.vendor}\n"
        f"Date: {invoice_data.date}\n"
        f"Total: {invoice_data.total}\n"
        f"Line Items: {[item.dict() for item in invoice_data.line_items]}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()