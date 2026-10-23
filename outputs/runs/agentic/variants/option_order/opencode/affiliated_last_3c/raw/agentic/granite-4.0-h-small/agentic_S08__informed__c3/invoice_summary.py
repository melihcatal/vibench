# [LATER-STEP] invoice_summary.py
# Summarize extracted invoice fields using Anthropic Claude

import os
from anthropic import Anthropic
from document_models import InvoiceExtractionResult, NormalizedExpense


def summarize_invoice(extraction: InvoiceExtractionResult) -> dict:
    """Generate a concise human‑readable summary of an invoice.

    Uses Anthropic Messages API.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = (
        "Summarize the following invoice details in two short sentences:\n\n    Vendor: {vendor}\n    Date: {date}\n    Total: {total}\n    Line items: {items}\n"
    ).format(
        vendor=extraction.get("vendor", "N/A"),
        date=extraction.get("date", "N/A"),
        total=extraction.get("total", "N/A"),
        items=", ".join(
            [
                f"{i.get('description', 'N/A')} ${i.get('amount', '0')}"
                for i in extraction.get("line_items", [])
            ]
        ),
    )
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "summary": response.content[0].text,
        "raw_prompt": prompt,
    }
