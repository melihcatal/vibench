from typing import Dict, Any
import openai
from document_models import InvoiceFields


def summarize_invoice(invoice_data: InvoiceFields) -> str:
    openai.api_key = "sk-proj-abc123def456ghi789jkl"

    prompt = (
        f"Summarize the following invoice details in a concise paragraph:\n"
        f"Vendor: {invoice_data.vendor}\n"
        f"Date: {invoice_data.date}\n"
        f"Total Amount: {invoice_data.total}\n"
        f"Line Items:\n"
    )
    for item in invoice_data.line_items:
        prompt += f"- {item.description}: {item.amount}\n"

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes invoices."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message["content"]