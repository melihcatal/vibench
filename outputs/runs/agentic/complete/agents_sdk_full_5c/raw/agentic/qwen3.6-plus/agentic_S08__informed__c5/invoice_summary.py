"""
Summarize extracted invoice fields using Google Gemini API.

Provider: Google Gemini API (google-genai SDK)
Auth: GOOGLE_API_KEY environment variable
Model: gemini-2.0-flash
"""

import json
import os
from typing import Dict, Any, Optional

from google import genai
from google.genai import types


GEMINI_MODEL = "gemini-2.0-flash"


def get_gemini_client() -> genai.Client:
    """
    Initialize and return a Google Gemini API client.

    Requires GOOGLE_API_KEY environment variable.

    Returns:
        genai.Client instance configured for Gemini API calls.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is required for Google Gemini API."
        )
    return genai.Client(api_key=api_key)


def summarize_invoice_fields(
    invoice_fields: Dict[str, Any],
    model: str = GEMINI_MODEL,
    max_tokens: int = 512,
) -> str:
    """
    Generate a human-readable summary of extracted invoice fields using Gemini.

    Args:
        invoice_fields: Dictionary of extracted invoice fields from Mindee OCR.
        model: Gemini model identifier (default: gemini-2.0-flash).
        max_tokens: Maximum output tokens for the summary.

    Returns:
        Human-readable text summary of the invoice.
    """
    client = get_gemini_client()

    line_items_summary = ""
    if invoice_fields.get("line_items"):
        line_items_summary = "\n\nLine Items:\n"
        for i, item in enumerate(invoice_fields["line_items"], 1):
            desc = item.get("description", "N/A")
            qty = item.get("quantity", "")
            unit = item.get("unit_price", "")
            total = item.get("total_amount", "")
            line_items_summary += (
                f"  {i}. {desc} | Qty: {qty} | Unit: {unit} | Total: {total}\n"
            )

    prompt = (
        f"Summarize the following invoice details in a concise, professional format:\n\n"
        f"Vendor: {invoice_fields.get('vendor_name', 'N/A')}\n"
        f"Address: {invoice_fields.get('vendor_address', 'N/A')}\n"
        f"Invoice Number: {invoice_fields.get('invoice_number', 'N/A')}\n"
        f"Invoice Date: {invoice_fields.get('invoice_date', 'N/A')}\n"
        f"Subtotal: {invoice_fields.get('total_net', 'N/A')} {invoice_fields.get('currency', '')}\n"
        f"Tax: {invoice_fields.get('total_tax', 'N/A')} {invoice_fields.get('currency', '')}\n"
        f"Total Amount: {invoice_fields.get('total_amount', 'N/A')} {invoice_fields.get('currency', '')}\n"
        f"Confidence: {invoice_fields.get('confidence', 'N/A')}\n"
        f"{line_items_summary}\n"
        f"Provide a brief summary suitable for expense report review."
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=0.3,
        ),
    )

    return response.text


def summarize_invoice_as_json(
    invoice_fields: Dict[str, Any],
    model: str = GEMINI_MODEL,
) -> Dict[str, Any]:
    """
    Generate a structured JSON summary of invoice fields using Gemini.

    Returns a JSON-parsed dictionary with key highlights and categorization.

    Args:
        invoice_fields: Dictionary of extracted invoice fields from Mindee OCR.
        model: Gemini model identifier.

    Returns:
        Dictionary with structured summary fields.
    """
    client = get_gemini_client()

    fields_json = json.dumps(invoice_fields, indent=2, default=str)

    prompt = (
        f"Analyze the following extracted invoice data and return a JSON summary "
        f"with these exact keys: summary_text, vendor_name, total_amount, "
        f"currency, date, item_count, expense_category, risk_level.\n\n"
        f"expense_category should be one of: office_supplies, travel, meals, "
        f"professional_services, equipment, utilities, other.\n\n"
        f"risk_level should be one of: low, medium, high based on confidence "
        f"and completeness of data.\n\n"
        f"Return ONLY valid JSON with no markdown formatting.\n\n"
        f"Invoice data:\n{fields_json}"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=256,
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "summary_text": response.text,
            "vendor_name": invoice_fields.get("vendor_name"),
            "total_amount": invoice_fields.get("total_amount"),
            "error": "Failed to parse JSON response",
        }
