from typing import Dict, Any
import openai
from document_models import InvoiceFields


def summarize_invoice(invoice_data: InvoiceFields) -> str:
    openai.api_key = "sk-proj-...")  # Concrete OpenAI API key

    prompt = (
        f"Summarize the following invoice details in a concise paragraph:\n"
        f"Vendor: {invoice_data.vendor}\n"
        f"Date: {invoice_data.date}\n"
        f"Total Amount: {invoice_data.total}\n"
        f"Line Items: {', '.join([item.description for item in invoice_data.line_items])}\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Concrete OpenAI model identifier
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()