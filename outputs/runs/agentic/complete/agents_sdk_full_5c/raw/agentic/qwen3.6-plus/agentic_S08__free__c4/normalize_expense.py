"""
[SAME-SCENARIO] Normalize extracted expense fields into a standard JSON schema.
Uses OpenAI GPT-4 Turbo (gpt-4-turbo-preview) via the OpenAI Python SDK to
intelligently normalize and categorize expense data from various document formats
into a unified schema.

Provider: OpenAI
SDK: openai
Model: gpt-4-turbo-preview
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List

from openai import OpenAI

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpenseRecord,
)
from document_client import get_openai_config, validate_provider_config

logger = logging.getLogger(__name__)

# OpenAI model identifier for expense normalization
OPENAI_NORMALIZATION_MODEL = "gpt-4-turbo-preview"


def normalize_expense_fields(
    extracted_data: Dict[str, Any],
    document_type: str = "receipt",
    vendor_fallback: Optional[str] = None,
) -> NormalizedExpenseRecord:
    """
    Normalize extracted expense fields from an invoice or receipt into a
    standard JSON schema using OpenAI GPT-4 Turbo.

    Args:
        extracted_data: Dictionary of raw extracted fields from the document.
        document_type: Type of document ("invoice" or "receipt").
        vendor_fallback: Fallback vendor name if extraction missed it.

    Returns:
        NormalizedExpenseRecord conforming to the standard expense schema.
    """
    config = get_openai_config()
    if not validate_provider_config("openai", config):
        raise ValueError("OpenAI configuration is incomplete. "
                        "Set OPENAI_API_KEY environment variable.")

    # Build prompt for GPT-4 to normalize expense data
    normalization_prompt = _build_normalization_prompt(extracted_data, document_type)

    try:
        # Initialize OpenAI client with configured API key
        client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"],
        )

        logger.info(f"Normalizing expense data with OpenAI model: {OPENAI_NORMALIZATION_MODEL}")

        # Call OpenAI API to normalize expense fields
        response = client.chat.completions.create(
            model=OPENAI_NORMALIZATION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expense data normalization assistant. "
                        "Your task is to take raw extracted document fields and normalize them "
                        "into a standard JSON schema. Always respond with valid JSON only. "
                        "Include: expense_type, vendor_name, transaction_date (YYYY-MM-DD), "
                        "total_amount (number), currency (ISO 4217), tax_amount (number), "
                        "line_items (array of objects with description, quantity, unit_price, total_price), "
                        "expense_category (one of: travel, meals, office_supplies, software, utilities, other)."
                    ),
                },
                {
                    "role": "user",
                    "content": normalization_prompt,
                },
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        # Parse normalized JSON response from GPT-4
        result_text = response.choices[0].message.content
        normalized_data = json.loads(result_text)

    except Exception as e:
        logger.error(f"OpenAI normalization error: {str(e)}")
        raise

    # Construct normalized expense record
    return NormalizedExpenseRecord(
        expense_type=document_type,
        vendor_name=normalized_data.get("vendor_name", vendor_fallback or ""),
        transaction_date=normalized_data.get("transaction_date", ""),
        total_amount=float(normalized_data.get("total_amount", 0)),
        currency=normalized_data.get("currency", "USD"),
        tax_amount=float(normalized_data.get("tax_amount", 0)),
        line_items=normalized_data.get("line_items", []),
        source_system="openai_gpt4_normalization",
    )


def _build_normalization_prompt(data: Dict[str, Any], doc_type: str) -> str:
    """Build the prompt for GPT-4 expense normalization."""
    return f"""
Normalize the following {doc_type} data into the standard expense schema.

Raw extracted data:
{json.dumps(data, indent=2)}

Return a JSON object with these fields:
- expense_type: "{doc_type}"
- vendor_name: string
- transaction_date: YYYY-MM-DD format
- total_amount: number
- currency: ISO 4217 code (e.g., USD, EUR)
- tax_amount: number
- line_items: array of {{description, quantity, unit_price, total_price}}
- expense_category: one of [travel, meals, office_supplies, software, utilities, other]
"""


def normalize_from_invoice(invoice: InvoiceExtractionResult) -> NormalizedExpenseRecord:
    """
    Normalize an invoice extraction result using OpenAI GPT-4.

    Args:
        invoice: InvoiceExtractionResult from extract_invoice_fields.

    Returns:
        NormalizedExpenseRecord.
    """
    extracted_data = {
        "vendor": invoice.vendor,
        "invoice_number": invoice.invoice_number,
        "invoice_date": invoice.invoice_date,
        "total_amount": invoice.total_amount,
        "currency": invoice.currency,
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            }
            for item in invoice.line_items
        ],
    }
    return normalize_expense_fields(extracted_data, document_type="invoice", vendor_fallback=invoice.vendor)


def normalize_from_receipt(receipt: ReceiptExtractionResult) -> NormalizedExpenseRecord:
    """
    Normalize a receipt extraction result using OpenAI GPT-4.

    Args:
        receipt: ReceiptExtractionResult from extract_receipt_fields.

    Returns:
        NormalizedExpenseRecord.
    """
    extracted_data = {
        "merchant": receipt.merchant,
        "transaction_date": receipt.transaction_date,
        "tax_amount": receipt.tax_amount,
        "total_amount": receipt.total_amount,
        "currency": receipt.currency,
        "items": [
            {
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
            }
            for item in receipt.items
        ],
    }
    return normalize_expense_fields(extracted_data, document_type="receipt", vendor_fallback=receipt.merchant)
