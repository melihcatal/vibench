import os
import json
from typing import Optional

from openai import OpenAI
from document_models import InvoiceExtractionResult

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def summarize_invoice_fields(
    invoice_result: InvoiceExtractionResult,
    additional_context: Optional[str] = None,
) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    line_items_text = ""
    for item in invoice_result.line_items:
        line_items_text += f"  - {item.description}: {item.quantity} x {item.unit_price} = {item.amount}\n"

    prompt = (
        f"Summarize the following extracted invoice data in a concise paragraph:\n"
        f"Vendor: {invoice_result.vendor_name}\n"
        f"Invoice ID: {invoice_result.invoice_id}\n"
        f"Date: {invoice_result.invoice_date}\n"
        f"Due Date: {invoice_result.due_date}\n"
        f"Subtotal: {invoice_result.subtotal}\n"
        f"Tax: {invoice_result.total_tax}\n"
        f"Total Amount: {invoice_result.total_amount} {invoice_result.currency}\n"
        f"Line Items:\n{line_items_text}"
    )

    if additional_context:
        prompt += f"\nAdditional Context: {additional_context}\n"

    prompt += "\nProvide a brief executive summary of this invoice suitable for expense reporting."

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that summarizes invoice data for expense reporting.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=256,
    )

    summary = response.choices[0].message.content.strip()
    return summary


def summarize_invoice_fields_batch(
    invoice_results: list,
) -> list:
    summaries = []
    for result in invoice_results:
        summaries.append(summarize_invoice_fields(result))
    return summaries


def summarize_invoice_to_json(
    invoice_result: InvoiceExtractionResult,
) -> dict:
    summary_text = summarize_invoice_fields(invoice_result)
    return {
        "vendor_name": invoice_result.vendor_name,
        "invoice_id": invoice_result.invoice_id,
        "invoice_date": invoice_result.invoice_date,
        "total_amount": invoice_result.total_amount,
        "currency": invoice_result.currency,
        "summary": summary_text,
        "line_item_count": len(invoice_result.line_items),
        "confidence": invoice_result.raw_confidence,
    }
