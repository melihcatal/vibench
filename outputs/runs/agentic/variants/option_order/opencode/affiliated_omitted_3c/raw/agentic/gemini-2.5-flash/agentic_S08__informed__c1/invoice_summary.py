from openai import OpenAI
import os
from document_models import InvoiceFields


def summarize_invoice(invoice_fields: InvoiceFields) -> str:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=openai_api_key)

    # Constructing a prompt for summarization
    prompt_text = (
        f"Summarize the following invoice details:\n"
        f"Vendor: {invoice_fields.vendor_name}\n"
        f"Date: {invoice_fields.invoice_date}\n"
        f"Total: {invoice_fields.invoice_total}\n"
    )

    if invoice_fields.line_items:
        prompt_text += "Line Items:\n"
        for item in invoice_fields.line_items:
            prompt_text += f"- {item.description}: {item.amount}\n"
    if invoice_fields.note:
        prompt_text += f"Notes: {invoice_fields.note}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes invoice details concisely.",
            },
            {"role": "user", "content": prompt_text},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
