import os
from datetime import datetime

from openai import OpenAI

from document_models import InvoiceExtraction, InvoiceSummary


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def summarize_invoice(invoice: InvoiceExtraction) -> InvoiceSummary:
    client = OpenAI(api_key=OPENAI_API_KEY)

    line_items_text = ""
    if invoice.line_items:
        items_lines = []
        for item in invoice.line_items:
            items_lines.append(
                f"- {item.description}: qty={item.quantity}, "
                f"unit_price={item.unit_price}, total={item.total}"
            )
        line_items_text = "\n".join(items_lines)
    else:
        line_items_text = "No line items extracted."

    prompt = (
        f"Summarize the following invoice data in 2-3 concise sentences. "
        f"Focus on the vendor, date, total amount, and notable line items.\n\n"
        f"Vendor: {invoice.vendor}\n"
        f"Date: {invoice.invoice_date}\n"
        f"Total Amount: {invoice.total_amount} {invoice.currency}\n"
        f"Tax: {invoice.tax_amount} {invoice.currency}\n"
        f"Line Items:\n{line_items_text}\n"
        f"Extraction Confidence: {invoice.confidence_overall:.2f}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an invoice summarization assistant. "
                    "Provide concise, factual summaries of invoice data. "
                    "Do not add information not present in the input."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    summary_text = response.choices[0].message.content.strip()

    return InvoiceSummary(
        vendor=invoice.vendor,
        invoice_date=invoice.invoice_date,
        total_amount=invoice.total_amount,
        line_item_count=len(invoice.line_items),
        summary_text=summary_text,
        generated_at=datetime.utcnow().isoformat(),
    )
