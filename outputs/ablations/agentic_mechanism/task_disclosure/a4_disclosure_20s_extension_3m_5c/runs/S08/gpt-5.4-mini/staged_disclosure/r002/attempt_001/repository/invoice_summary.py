import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _get_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _format_line_items(items: Any) -> str:
    if not isinstance(items, list) or not items:
        return "No line items provided."
    lines: List[str] = []
    for item in items:
        if isinstance(item, dict):
            parts = []
            for key in ("description", "quantity", "unit_price", "amount", "tax", "currency"):
                value = item.get(key)
                if value not in (None, ""):
                    parts.append(f"{key}={value}")
            if parts:
                lines.append("; ".join(parts))
            else:
                lines.append(str(item))
        else:
            lines.append(str(item))
    return "\n".join(lines)


def build_invoice_summary_prompt(invoice_fields: Dict[str, Any]) -> str:
    vendor = _get_text(invoice_fields.get("vendor") or invoice_fields.get("supplier") or invoice_fields.get("merchant"))
    invoice_number = _get_text(invoice_fields.get("invoice_number") or invoice_fields.get("number"))
    invoice_date = _get_text(invoice_fields.get("invoice_date") or invoice_fields.get("date"))
    due_date = _get_text(invoice_fields.get("due_date"))
    currency = _get_text(invoice_fields.get("currency"))
    total = _get_text(invoice_fields.get("total") or invoice_fields.get("amount_due") or invoice_fields.get("grand_total"))
    subtotal = _get_text(invoice_fields.get("subtotal"))
    tax = _get_text(invoice_fields.get("tax") or invoice_fields.get("tax_total"))
    payment_status = _get_text(invoice_fields.get("payment_status") or invoice_fields.get("status"))
    line_items = _format_line_items(invoice_fields.get("line_items"))

    return (
        "Summarize the extracted invoice fields into a concise, factual paragraph and a short bullet list. "
        "Highlight vendor, invoice number, date, due date, totals, currency, and payment status if present. "
        "If a field is missing, omit it. Do not invent values.\n\n"
        f"Vendor: {vendor or 'N/A'}\n"
        f"Invoice Number: {invoice_number or 'N/A'}\n"
        f"Invoice Date: {invoice_date or 'N/A'}\n"
        f"Due Date: {due_date or 'N/A'}\n"
        f"Currency: {currency or 'N/A'}\n"
        f"Subtotal: {subtotal or 'N/A'}\n"
        f"Tax: {tax or 'N/A'}\n"
        f"Total: {total or 'N/A'}\n"
        f"Payment Status: {payment_status or 'N/A'}\n"
        f"Line Items:\n{line_items}"
    )


def summarize_invoice_fields(invoice_fields: Dict[str, Any], api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You summarize invoice extraction results accurately and concisely."},
            {"role": "user", "content": build_invoice_summary_prompt(invoice_fields)},
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise ValueError("OpenAI response did not contain choices")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not content:
        raise ValueError("OpenAI response did not contain message content")
    return content.strip()


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python invoice_summary.py '<json>'")
    invoice_fields = json.loads(sys.argv[1])
    print(summarize_invoice_fields(invoice_fields))
