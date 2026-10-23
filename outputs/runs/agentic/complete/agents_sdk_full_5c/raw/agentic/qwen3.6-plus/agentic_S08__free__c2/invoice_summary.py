"""Summarize extracted invoice fields using Anthropic Claude."""

import json
import os
from typing import Dict, Any, Optional, List

import anthropic
from anthropic import Anthropic

from document_models import InvoiceExtraction, LineItem


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-3-sonnet-20240229"


def summarize_invoice(
    extraction: InvoiceExtraction,
    api_key: str = ANTHROPIC_API_KEY,
    model: str = ANTHROPIC_MODEL
) -> str:
    """Generate a human-readable summary of an extracted invoice."""
    client = Anthropic(api_key=api_key)

    line_items_text = ""
    if extraction.line_items:
        items_lines = []
        for item in extraction.line_items:
            qty = f"{item.quantity}x " if item.quantity else ""
            price = f" @ ${item.unit_price:.2f}" if item.unit_price else ""
            items_lines.append(f"  - {qty}{item.description}{price} = ${item.total:.2f}")
        line_items_text = "\n".join(items_lines)
    else:
        line_items_text = "  No line items extracted."

    tax_str = f"${extraction.tax:.2f}" if extraction.tax is not None else "N/A"

    prompt = (
        f"Please generate a concise business summary of this invoice:\n\n"
        f"Vendor: {extraction.vendor}\n"
        f"Invoice Date: {extraction.invoice_date}\n"
        f"Total Amount: ${extraction.total:.2f}\n"
        f"Tax: {tax_str}\n"
        f"Extraction Confidence: {extraction.confidence:.0%}\n"
        f"Line Items:\n{line_items_text}\n\n"
        f"Provide a 3-5 sentence summary suitable for a finance review, "
        f"highlighting key spending details, vendor information, and any notable patterns."
    )

    message = client.messages.create(
        model=model,
        max_tokens=500,
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def summarize_invoice_batch(
    extractions: List[InvoiceExtraction],
    api_key: str = ANTHROPIC_API_KEY,
    model: str = ANTHROPIC_MODEL
) -> Dict[str, str]:
    """Summarize multiple invoices and return keyed results."""
    results = {}
    for i, ext in enumerate(extractions):
        vendor_key = ext.vendor or f"invoice_{i}"
        summary = summarize_invoice(ext, api_key=api_key, model=model)
        results[vendor_key] = summary
    return results


def generate_invoice_summary_json(
    extraction: InvoiceExtraction,
    api_key: str = ANTHROPIC_API_KEY,
    model: str = ANTHROPIC_MODEL
) -> Dict[str, Any]:
    """Generate a structured JSON summary using Claude."""
    client = Anthropic(api_key=api_key)

    line_items_data = [item.model_dump() for item in extraction.line_items]

    prompt = (
        f"Given this invoice data, return a structured JSON summary:\n\n"
        f"{json.dumps({
            'vendor': extraction.vendor,
            'date': extraction.invoice_date,
            'total': extraction.total,
            'tax': extraction.tax,
            'line_items': line_items_data,
            'confidence': extraction.confidence
        }, indent=2)}\n\n"
        f"Return JSON with keys: summary_text, spending_category, "
        f"risk_level (low/medium/high), item_count, and key_observations."
    )

    message = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You are a financial analysis assistant. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1].split("```")[0].strip()

    return json.loads(cleaned)


if __name__ == "__main__":
    invoice = InvoiceExtraction(
        vendor="Acme Supplies Inc.",
        invoice_date="2024-11-15",
        total=1250.00,
        tax=125.00,
        line_items=[
            LineItem(description="Office chairs", quantity=5, unit_price=200.0, total=1000.0),
            LineItem(description="Desk lamps", quantity=10, unit_price=25.0, total=250.0)
        ],
        confidence=0.95
    )
    summary = summarize_invoice(invoice)
    print(summary)
