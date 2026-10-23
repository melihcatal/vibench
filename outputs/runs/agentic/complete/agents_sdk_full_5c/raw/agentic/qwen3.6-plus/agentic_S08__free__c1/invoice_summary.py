"""
Summarize extracted invoice fields using OpenAI GPT-4o.

Generates a human-readable summary of invoice data including vendor information,
financial totals, and line item overview using OpenAI's chat completion API.

Provider: OpenAI
Model: gpt-4o
SDK: openai
API: https://api.openai.com/v1/chat/completions
"""

import json
import os
from typing import Optional

from openai import OpenAI

from document_models import ExtractedInvoiceField, NormalizedExpense


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def create_invoice_summary_prompt(extracted: ExtractedInvoiceField) -> str:
    """
    Create a prompt for summarizing invoice data.

    Args:
        extracted: ExtractedInvoiceField from Azure Document Intelligence.

    Returns:
        Formatted prompt string for OpenAI chat completion.
    """
    line_items_summary = ""
    if extracted.line_items:
        items_text = []
        for i, item in enumerate(extracted.line_items, 1):
            desc = item.get("Description", "N/A")
            qty = item.get("Quantity", "")
            amount = item.get("Amount", "N/A")
            items_text.append(f"  {i}. {desc} (Qty: {qty}, Amount: {amount})")
        line_items_summary = "\n".join(items_text)
    else:
        line_items_summary = "  No line items provided."

    prompt = f"""Summarize the following invoice extraction results in a clear, concise format:

Vendor: {extracted.vendor_name or 'N/A'}
Vendor Address: {extracted.vendor_address or 'N/A'}
Invoice ID: {extracted.invoice_id or 'N/A'}
Invoice Date: {extracted.invoice_date or 'N/A'}
Due Date: {extracted.due_date or 'N/A'}

Financial Summary:
  Subtotal: {extracted.sub_total if extracted.sub_total is not None else 'N/A'}
  Tax: {extracted.tax if extracted.tax is not None else 'N/A'}
  Total: {extracted.total if extracted.total is not None else 'N/A'}
  Currency: {extracted.currency or 'N/A'}

Line Items:
{line_items_summary}

Provide a brief summary that highlights the key information, including:
1. Who the invoice is from
2. The total amount due
3. The number of line items
4. Any notable details (due date, high-value items, etc.)

Keep the summary to 2-3 sentences."""

    return prompt


def summarize_invoice(
    extracted: ExtractedInvoiceField,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> str:
    """
    Generate a summary of extracted invoice fields using OpenAI GPT-4o.

    Args:
        extracted: ExtractedInvoiceField from Azure Document Intelligence analysis.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI model to use. Defaults to gpt-4o.

    Returns:
        Human-readable summary string of the invoice.

    Raises:
        ValueError: If OpenAI API key is not provided.
        openai.OpenAIError: If the OpenAI API call fails.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=key)
    prompt = create_invoice_summary_prompt(extracted)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that summarizes invoice data. "
                    "Provide clear, concise summaries of financial documents."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    summary = response.choices[0].message.content
    return summary or "Unable to generate summary."


def summarize_normalized_expense(
    expense: NormalizedExpense,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> str:
    """
    Generate a summary from a normalized expense record using OpenAI GPT-4o.

    Args:
        expense: NormalizedExpense record.
        api_key: OpenAI API key.
        model: OpenAI model to use. Defaults to gpt-4o.

    Returns:
        Human-readable summary string.
    """
    prompt = f"""Summarize the following expense record:

Vendor: {expense.vendor}
Date: {expense.date}
Total Amount: {expense.total_amount} {expense.currency}
Tax Amount: {expense.tax_amount}
Document Type: {expense.document_type}

Line Items:
{json.dumps(expense.line_items, indent=2)}

Provide a brief 2-3 sentence summary of this expense."""

    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OpenAI API key is required.")

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that summarizes expense records. "
                    "Provide clear, concise summaries."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    return response.choices[0].message.content or "Unable to generate summary."
