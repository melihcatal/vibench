import os

from mistralai import Mistral

from document_models import InvoiceExtraction

MISTRAL_MODEL = "mistral-large-latest"


def summarize_invoice_fields(
    invoice: InvoiceExtraction, additional_context: str = ""
) -> str:
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    client = Mistral(api_key=api_key)
    line_items_text = ""
    for item in invoice.line_items:
        line_items_text += f"- {item.description.value}: {item.quantity.value} x {item.unit_price.value} = {item.total_price.value}\n"
    prompt = (
        f"Summarize the following invoice data in a concise paragraph:\n"
        f"Vendor: {invoice.vendor_name.value}\n"
        f"Date: {invoice.invoice_date.value}\n"
        f"Total: {invoice.invoice_total.value}\n"
        f"Line Items:\n{line_items_text}"
    )
    if additional_context:
        prompt += f"\nAdditional context: {additional_context}"
    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an invoice analysis assistant. Provide clear, concise summaries of invoice data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=256,
    )
    return response.choices[0].message.content


def generate_invoice_summary_batch(invoices: list[InvoiceExtraction]) -> list[str]:
    summaries = []
    for invoice in invoices:
        summary = summarize_invoice_fields(invoice)
        summaries.append(summary)
    return summaries
