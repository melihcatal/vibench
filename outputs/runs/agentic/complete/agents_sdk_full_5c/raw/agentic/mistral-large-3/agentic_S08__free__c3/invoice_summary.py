from typing import Dict, Any
from openai import OpenAI
from document_models import InvoiceExtractionResponse


client = OpenAI(api_key=open(".openai_api_key").read().strip())


def summarize_invoice(invoice_data: InvoiceExtractionResponse) -> str:
    prompt = (
        f"Summarize the following invoice details in a concise paragraph:\n"
        f"Vendor: {invoice_data.vendor}\n"
        f"Date: {invoice_data.date}\n"
        f"Total: {invoice_data.total}\n"
        f"Line Items: {[item.dict() for item in invoice_data.line_items]}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()