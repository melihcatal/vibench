import os
import json
from openai import OpenAI
from document_models import InvoiceExtractionResult

OPENAI_MODEL = "gpt-4o"


def build_invoice_summary_prompt(invoice_result: InvoiceExtractionResult) -> str:
    line_items_summary = ""
    if invoice_result.line_items:
        items_text = "\n".join(
            f"  - {item.description}: qty={item.quantity}, unit_price={item.unit_price}, amount={item.amount}"
            for item in invoice_result.line_items
        )
        line_items_summary = f"\nLine Items:\n{items_text}"

    prompt = (
        f"Summarize the following invoice extraction results in a concise paragraph:\n"
        f"Vendor: {invoice_result.vendor_name.value}\n"
        f"Invoice ID: {invoice_result.invoice_id.value}\n"
        f"Date: {invoice_result.invoice_date.value}\n"
        f"Subtotal: {invoice_result.invoice_sub_total.value}\n"
        f"Tax: {invoice_result.invoice_tax.value}\n"
        f"Total: {invoice_result.invoice_total.value}\n"
        f"Billing Address: {invoice_result.billing_address.value}"
        f"{line_items_summary}\n"
        f"Provide a clear, professional summary suitable for expense reporting."
    )
    return prompt


def summarize_invoice(
    invoice_result: InvoiceExtractionResult, model=OPENAI_MODEL
) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set for OpenAI chat completions")

    client = OpenAI(api_key=api_key)
    prompt = build_invoice_summary_prompt(invoice_result)

    response = client.chat.completions.create(
        model=model,
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


def summarize_invoice_from_dict(invoice_data: dict, model=OPENAI_MODEL) -> str:
    from document_models import FieldWithConfidence, LineItem

    invoice_result = InvoiceExtractionResult(
        vendor_name=FieldWithConfidence(
            value=invoice_data.get("vendor_name", {}).get("value", "")
        ),
        invoice_date=FieldWithConfidence(
            value=invoice_data.get("invoice_date", {}).get("value", "")
        ),
        invoice_total=FieldWithConfidence(
            value=invoice_data.get("invoice_total", {}).get("value", 0.0)
        ),
        invoice_sub_total=FieldWithConfidence(
            value=invoice_data.get("invoice_sub_total", {}).get("value", 0.0)
        ),
        invoice_tax=FieldWithConfidence(
            value=invoice_data.get("invoice_tax", {}).get("value", 0.0)
        ),
        invoice_id=FieldWithConfidence(
            value=invoice_data.get("invoice_id", {}).get("value", "")
        ),
        billing_address=FieldWithConfidence(
            value=invoice_data.get("billing_address", {}).get("value", "")
        ),
    )

    raw_items = invoice_data.get("line_items", [])
    for item_data in raw_items:
        invoice_result.line_items.append(
            LineItem(
                description=item_data.get("description", ""),
                quantity=item_data.get("quantity", 0.0),
                unit_price=item_data.get("unit_price", 0.0),
                amount=item_data.get("amount", 0.0),
            )
        )

    return summarize_invoice(invoice_result, model=model)
