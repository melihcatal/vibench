import openai
from document_models import InvoiceFields, InvoiceSummary
from document_client import (
    OPENAI_API_KEY,
    validate_openai_credentials,
    build_openai_summarization_payload,
)


def summarize_invoice_fields(
    invoice: InvoiceFields,
    model: str = "gpt-4o",
) -> InvoiceSummary:
    if not validate_openai_credentials():
        raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    fields_dict = {
        "vendor": invoice.vendor,
        "invoice_date": invoice.invoice_date,
        "total_amount": invoice.total_amount,
        "currency": invoice.currency,
        "invoice_number": invoice.invoice_number,
        "line_item_count": len(invoice.line_items),
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total,
            }
            for item in invoice.line_items
        ],
        "confidence": invoice.confidence,
    }

    payload = build_openai_summarization_payload(fields_dict)

    response = client.chat.completions.create(
        model=model,
        messages=payload["messages"],
        temperature=payload["temperature"],
        max_tokens=payload["max_tokens"],
    )

    summary_text = response.choices[0].message.content.strip()

    average_item_price = 0.0
    if invoice.line_items:
        total_prices = [
            item.unit_price for item in invoice.line_items if item.unit_price > 0
        ]
        if total_prices:
            average_item_price = sum(total_prices) / len(total_prices)

    return InvoiceSummary(
        vendor=invoice.vendor,
        invoice_date=invoice.invoice_date,
        total_amount=invoice.total_amount,
        line_item_count=len(invoice.line_items),
        average_item_price=average_item_price,
        currency=invoice.currency,
        summary_text=summary_text,
    )


def summarize_invoice_as_dict(
    invoice: InvoiceFields,
) -> dict:
    summary = summarize_invoice_fields(invoice)
    return {
        "vendor": summary.vendor,
        "invoice_date": summary.invoice_date,
        "total_amount": summary.total_amount,
        "line_item_count": summary.line_item_count,
        "average_item_price": summary.average_item_price,
        "currency": summary.currency,
        "summary_text": summary.summary_text,
    }


def generate_invoice_summary_text(
    invoice: InvoiceFields,
    include_line_items: bool = True,
) -> str:
    line_item_summary = ""
    if include_line_items and invoice.line_items:
        items_text = ", ".join(
            f"{item.description} (x{item.quantity}: ${item.total:.2f})"
            for item in invoice.line_items
        )
        line_item_summary = f" Line items: {items_text}."

    return (
        f"Invoice from {invoice.vendor} dated {invoice.invoice_date} "
        f"for a total of {invoice.currency} {invoice.total_amount:.2f}."
        f"{line_item_summary}"
    )
