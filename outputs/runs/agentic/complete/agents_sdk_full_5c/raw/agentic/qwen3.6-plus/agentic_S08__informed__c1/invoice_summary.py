"""
[LATER-STEP] Summarize extracted invoice fields using Anthropic Claude LLM.

Uses the Anthropic Messages API to generate a human-readable summary of extracted
invoice fields including vendor info, line items, totals, and any anomalies.
Provider: Anthropic - Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-5-sonnet-20241022
"""

from __future__ import annotations

import os
from typing import Optional

import anthropic
from anthropic import Anthropic

from document_models import InvoiceExtractionResult


def _build_invoice_context(invoice: InvoiceExtractionResult) -> str:
    """Build a text context string from the extracted invoice data."""
    lines = []

    lines.append("INVOICE SUMMARY REQUEST")
    lines.append("=" * 40)

    if invoice.vendor:
        lines.append(f"\nVendor: {invoice.vendor.name or 'N/A'}")
        if invoice.vendor.address:
            lines.append(f"Address: {invoice.vendor.address}")
        if invoice.vendor.tax_id:
            lines.append(f"Tax ID: {invoice.vendor.tax_id}")

    lines.append(f"\nInvoice Number: {invoice.invoice_number or 'N/A'}")
    lines.append(f"Invoice Date: {invoice.invoice_date or 'N/A'}")
    if invoice.due_date:
        lines.append(f"Due Date: {invoice.due_date}")

    lines.append(f"\nCurrency: {invoice.currency or 'N/A'}")
    lines.append(f"Subtotal: {invoice.subtotal or 'N/A'}")
    lines.append(f"Tax Amount: {invoice.tax_amount or 'N/A'}")
    lines.append(f"Total Amount: {invoice.total_amount or 'N/A'}")

    if invoice.line_items:
        lines.append(f"\nLine Items ({len(invoice.line_items)} items):")
        for i, item in enumerate(invoice.line_items, 1):
            lines.append(
                f"  {i}. {item.description} "
                f"{'| Qty: ' + str(item.quantity) if item.quantity else ''} "
                f"{'| Unit: ' + str(item.unit_price) if item.unit_price else ''} "
                f"{'| Total: ' + str(item.total_price) if item.total_price else ''}"
            )
    else:
        lines.append("\nNo line items extracted.")

    if invoice.confidence_scores:
        avg_conf = sum(s.value for s in invoice.confidence_scores.values()) / len(invoice.confidence_scores)
        lines.append(f"\nAverage Extraction Confidence: {avg_conf:.2%}")

    return "\n".join(lines)


def summarize_invoice(
    invoice: InvoiceExtractionResult,
    api_key: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 1024,
    include_recommendations: bool = True,
) -> str:
    """
    Generate a human-readable summary of extracted invoice fields using Anthropic Claude.

    Uses the Anthropic Messages API with the claude-3-5-sonnet-20241022 model to
    produce a concise summary of the invoice data, highlighting key fields and
    optionally providing recommendations.

    Args:
        invoice: An InvoiceExtractionResult from Mindee Invoice OCR.
        api_key: Optional Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.
        model: Anthropic model identifier. Default: claude-3-5-sonnet-20241022.
        max_tokens: Maximum tokens for the response.
        include_recommendations: Whether to include validation recommendations.

    Returns:
        A human-readable summary string of the invoice.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError(
            "Anthropic API key not found. Set the ANTHROPIC_API_KEY environment variable."
        )

    client = Anthropic(api_key=key)

    context = _build_invoice_context(invoice)

    instruction = (
        "You are a financial document analyst. Summarize the following extracted invoice data "
        "in a clear, structured format. Highlight:\n"
        "- Key vendor information\n"
        "- Invoice totals and dates\n"
        "- Notable line items\n"
        "- Any data quality concerns based on the extraction confidence\n"
    )
    if include_recommendations:
        instruction += (
            "\nAlso provide brief recommendations for follow-up actions, such as:\n"
            "- Fields that may need manual verification\n"
            "- Any discrepancies between subtotal, tax, and total\n"
            "- Unusual patterns in line items\n"
        )

    messages = [
        {"role": "user", "content": f"{instruction}\n\n---\n{context}"}
    ]

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
        system="You are a precise financial document summarizer. Provide structured, concise summaries.",
    )

    summary_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            summary_text += block.text

    return summary_text


def summarize_invoice_short(
    invoice: InvoiceExtractionResult,
    api_key: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
) -> str:
    """
    Generate a brief one-paragraph summary of an invoice using Anthropic Claude.

    Args:
        invoice: An InvoiceExtractionResult from Mindee Invoice OCR.
        api_key: Optional Anthropic API key.
        model: Anthropic model identifier.

    Returns:
        A concise one-paragraph summary string.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError("Set ANTHROPIC_API_KEY for Anthropic Claude access.")

    client = Anthropic(api_key=key)

    context = _build_invoice_context(invoice)

    response = client.messages.create(
        model=model,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Provide a single-paragraph summary of this invoice. "
                    f"Include vendor, total, date, and key line items.\n\n{context}"
                ),
            }
        ],
    )

    return "".join(
        block.text for block in response.content if hasattr(block, "text")
    )
