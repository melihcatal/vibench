"""Summarize extracted invoice fields using Mistral Chat API.

Uses Mistral AI chat models (mistral-large-latest) to generate a human-readable
summary of invoice data including vendor, date, total, and line items.
"""

import os
import json
from typing import Optional
from mistralai import Mistral
from document_models import InvoiceExtractionResult


MISTRAL_MODEL = "mistral-large-latest"


def build_invoice_prompt(extraction: InvoiceExtractionResult) -> str:
    """Build a prompt for the Mistral model from extraction results."""
    items_text = ""
    for item in extraction.line_items:
        items_text += (
            f"  - {item.description}: {item.quantity} x ${item.unit_price:.2f} "
            f"= ${item.amount:.2f}\n"
        )

    prompt = (
        f"Summarize the following invoice data in a concise paragraph:\n\n"
        f"Vendor: {extraction.vendor_name}\n"
        f"Invoice Date: {extraction.invoice_date}\n"
        f"Total Amount: ${extraction.total_amount:.2f}\n"
        f"Number of Line Items: {len(extraction.line_items)}\n"
        f"Line Items:\n{items_text}\n"
        f"Extraction Confidence: {extraction.confidence:.2f}\n\n"
        f"Provide a brief summary suitable for an expense report."
    )
    return prompt


def summarize_invoice(
    extraction: InvoiceExtractionResult,
    model: str = MISTRAL_MODEL,
) -> str:
    """Generate a summary of extracted invoice fields using Mistral Chat API.

    Connects to Mistral AI via the mistralai SDK using model mistral-large-latest.
    Authentication via MISTRAL_API_KEY environment variable.

    Args:
        extraction: The InvoiceExtractionResult to summarize.
        model: The Mistral model to use (default: mistral-large-latest).

    Returns:
        Generated summary text.
    """
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        raise EnvironmentError("MISTRAL_API_KEY environment variable is not set")

    client = Mistral(api_key=api_key)

    prompt = build_invoice_prompt(extraction)

    response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that summarizes invoice data concisely for expense reporting.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.3,
    )

    if response.choices and response.choices[0].message:
        return response.choices[0].message.content.strip()

    return ""


def summarize_invoice_from_dict(
    invoice_data: dict,
    model: str = MISTRAL_MODEL,
) -> str:
    """Summarize invoice data from a dictionary using Mistral Chat API.

    Args:
        invoice_data: Dictionary with keys: vendor_name, invoice_date, total_amount, line_items.
        model: Mistral model identifier.

    Returns:
        Generated summary text.
    """
    line_items = []
    for item in invoice_data.get("line_items", []):
        line_items.append(
            {
                "description": item.get("description", ""),
                "quantity": float(item.get("quantity", 0.0)),
                "unit_price": float(item.get("unit_price", 0.0)),
                "amount": float(item.get("amount", 0.0)),
            }
        )

    extraction = InvoiceExtractionResult(
        vendor_name=invoice_data.get("vendor_name", ""),
        invoice_date=invoice_data.get("invoice_date", ""),
        total_amount=float(invoice_data.get("total_amount", 0.0)),
        line_items=[],
        confidence=float(invoice_data.get("confidence", 0.0)),
        raw_fields=invoice_data.get("raw_fields", {}),
    )
    # Set line items manually since we can't pass dicts directly
    extraction.line_items = line_items

    return summarize_invoice(extraction, model=model)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        from extract_invoice_fields import extract_invoice_fields
        result = extract_invoice_fields(sys.argv[1])
        summary = summarize_invoice(result)
        print(summary)
