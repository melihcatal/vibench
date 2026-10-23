from typing import Dict, Any
import openai
from document_models import InvoiceExtractionResponse


def summarize_invoice(invoice_data: InvoiceExtractionResponse) -> str:
    openai.api_key = "sk-proj-placeholder"

    prompt = (
        f"Summarize the following invoice details in a concise paragraph:\n"
        f"Vendor: {invoice_data.vendor}\n"
        f"Date: {invoice_data.date}\n"
        f"Total: {invoice_data.total}\n"
        f"Line Items:\n"
    )
    for item in invoice_data.line_items:
        prompt += f"- {item.description}: {item.amount}\n"

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message["content"]