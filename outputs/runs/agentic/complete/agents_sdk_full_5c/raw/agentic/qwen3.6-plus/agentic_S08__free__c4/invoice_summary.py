"""
[LATER-STEP] Summarize extracted invoice fields.
Uses OpenAI GPT-4o (gpt-4o) via the OpenAI Python SDK to generate concise,
human-readable summaries of extracted invoice data including vendor details,
totals, and line item overviews.

Provider: OpenAI
SDK: openai
Model: gpt-4o
"""

import os
import json
import logging
from typing import Optional, Dict, Any

from openai import OpenAI

from document_models import InvoiceExtractionResult, NormalizedExpenseRecord
from document_client import get_openai_config, validate_provider_config

logger = logging.getLogger(__name__)

# OpenAI GPT-4o model identifier for summarization
OPENAI_SUMMARY_MODEL = "gpt-4o"


def summarize_invoice(
    invoice: InvoiceExtractionResult,
    include_line_items: bool = True,
    max_summary_length: int = 300,
) -> str:
    """
    Generate a concise summary of extracted invoice fields using OpenAI GPT-4o.

    Args:
        invoice: InvoiceExtractionResult from extract_invoice_fields.
        include_line_items: Whether to include line item details in summary.
        max_summary_length: Maximum character length for the summary.

    Returns:
        Human-readable summary string of the invoice.
    """
    config = get_openai_config()
    if not validate_provider_config("openai", config):
        raise ValueError("OpenAI configuration is incomplete. "
                        "Set OPENAI_API_KEY environment variable.")

    # Build invoice data for summarization
    invoice_data = {
        "vendor": invoice.vendor,
        "invoice_number": invoice.invoice_number,
        "invoice_date": invoice.invoice_date,
        "total_amount": f"{invoice.currency} {invoice.total_amount:.2f}",
        "currency": invoice.currency,
    }

    if include_line_items and invoice.line_items:
        invoice_data["line_items"] = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "total": item.total_price,
            }
            for item in invoice.line_items[:10]  # Limit to 10 items
        ]
        invoice_data["total_line_items"] = len(invoice.line_items)

    # Build summary prompt
    prompt = f"""
Create a concise summary of this invoice in under {max_summary_length} characters.

Invoice Data:
{json.dumps(invoice_data, indent=2)}

Include: vendor name, invoice date, total amount, number of line items,
and a brief description of the primary purchases. Use a professional tone.
"""

    try:
        # Initialize OpenAI client
        client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"],
        )

        logger.info(f"Generating invoice summary with OpenAI model: {OPENAI_SUMMARY_MODEL}")

        # Call OpenAI GPT-4o for summarization
        response = client.chat.completions.create(
            model=OPENAI_SUMMARY_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an invoice summarization assistant. Generate clear, concise summaries of invoice data for expense reports.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.3,
            max_tokens=200,
        )

        summary = response.choices[0].message.content.strip()
        logger.info(f"Invoice summary generated: {len(summary)} characters")
        return summary

    except Exception as e:
        logger.error(f"OpenAI GPT-4o summary generation error: {str(e)}")
        raise


def summarize_normalized_expense(record: NormalizedExpenseRecord) -> str:
    """
    Generate a summary from a normalized expense record using OpenAI GPT-4o.

    Args:
        record: NormalizedExpenseRecord to summarize.

    Returns:
        Human-readable summary string.
    """
    record_data = {
        "expense_type": record.expense_type,
        "vendor_name": record.vendor_name,
        "transaction_date": record.transaction_date,
        "total_amount": f"{record.currency} {record.total_amount:.2f}",
        "line_items_count": len(record.line_items),
    }

    prompt = f"""
Create a brief expense summary in under 150 characters.

Expense Data:
{json.dumps(record_data, indent=2)}
"""

    config = get_openai_config()
    client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])

    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expense summarization assistant. Create very brief summaries for expense records.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=100,
    )

    return response.choices[0].message.content.strip()


def batch_summarize_invoices(invoices: list) -> list:
    """
    Summarize multiple invoices in a batch using OpenAI GPT-4o.

    Args:
        invoices: List of InvoiceExtractionResult objects.

    Returns:
        List of (InvoiceExtractionResult, summary) tuples.
    """
    results = []
    for invoice in invoices:
        try:
            summary = summarize_invoice(invoice)
            results.append((invoice, summary))
        except Exception as e:
            logger.error(f"Failed to summarize invoice {invoice.invoice_number}: {str(e)}")
            results.append((invoice, f"Summary unavailable: {str(e)}"))
    return results
