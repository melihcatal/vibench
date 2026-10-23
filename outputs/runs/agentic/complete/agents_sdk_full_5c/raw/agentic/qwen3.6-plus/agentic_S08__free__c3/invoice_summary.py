"""Summarize extracted invoice fields using Anthropic Claude API."""

import os
import json
import anthropic
from document_models import InvoiceExtractionResponse


def summarize_invoice(invoice: InvoiceExtractionResponse) -> dict:
    """Summarize extracted invoice fields into a concise text summary using Anthropic Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    line_items_summary = ""
    if invoice.line_items:
        line_items_summary = "\n".join(
            f"- {item.description}: {item.quantity} x {item.unit_price} = {item.total_price}"
            for item in invoice.line_items
        )
    else:
        line_items_summary = "No line items extracted."

    invoice_data = json.dumps(invoice.to_dict(), indent=2, default=str)

    prompt = f"""You are a document processing assistant. Create a concise executive summary of this extracted invoice.

Invoice data:
{invoice_data}

Line items:
{line_items_summary}

Provide a summary with:
1. Vendor name and invoice date
2. Total amount and any notable line items
3. Brief risk assessment (e.g., high-value invoice, unusual line items, missing fields)
4. One-sentence action recommendation

Format the output as a structured JSON object with keys: "summary", "vendor", "date", "total", "risk_level", "action". Keep it concise."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0.2,
        system="You summarize invoice data into structured JSON. Always return valid JSON only.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    content = message.content[0].text.strip() if message.content else ""
    if content.startswith("```json"):
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif content.startswith("```"):
        content = content.split("```", 1)[1].split("```", 1)[0].strip()

    try:
        summary_dict = json.loads(content)
    except json.JSONDecodeError:
        summary_dict = {
            "summary": content,
            "vendor": invoice.vendor,
            "date": invoice.invoice_date,
            "total": invoice.total_amount,
            "risk_level": "unknown",
            "action": "Review manually",
        }

    return summary_dict


def generate_invoice_digest(invoices: list[InvoiceExtractionResponse]) -> str:
    """Generate a digest summarizing multiple invoices using Anthropic Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    invoices_text = ""
    for i, inv in enumerate(invoices, 1):
        invoices_text += f"\nInvoice {i}: {inv.vendor} | {inv.invoice_date} | {inv.total_amount}\n"

    prompt = f"""Summarize the following set of extracted invoices into a digest:

{invoices_text}

Provide:
- Total number of invoices
- Aggregate total amount
- Top vendors by count
- Any flagged invoices requiring attention
- Date range covered

Return plain text summary."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0.1,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return message.content[0].text.strip() if message.content else ""


if __name__ == "__main__":
    sample = InvoiceExtractionResponse(
        vendor="Acme Supplies Inc",
        invoice_date="2024-03-15",
        total_amount="$4,521.50",
        invoice_id="INV-2024-0315",
        line_items=[],
        confidence=0.92,
        provider="aws_textract",
    )
    result = summarize_invoice(sample)
    print(json.dumps(result, indent=2))
