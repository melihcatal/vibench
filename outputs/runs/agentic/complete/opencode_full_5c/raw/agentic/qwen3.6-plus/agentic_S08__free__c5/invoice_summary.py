import os
from typing import List, Dict, Any, Optional
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def summarize_invoice_fields(
    invoice_data: Dict[str, Any], model: str = OPENAI_MODEL
) -> str:
    client = get_openai_client()

    vendor_name = invoice_data.get("vendor_name", "Unknown")
    invoice_id = invoice_data.get("invoice_id", "N/A")
    invoice_date = invoice_data.get("invoice_date", "N/A")
    total = invoice_data.get("total", 0.0)
    tax = invoice_data.get("tax", 0.0)
    line_items = invoice_data.get("line_items", [])

    line_items_text = "\n".join(
        f"- {item.get('description', 'Item')}: {item.get('quantity', 0)} x ${item.get('unit_price', 0):.2f} = ${item.get('amount', 0):.2f}"
        for item in line_items
    )

    prompt = f"""Summarize the following invoice in a concise paragraph:

Vendor: {vendor_name}
Invoice ID: {invoice_id}
Date: {invoice_date}
Total: ${total:.2f}
Tax: ${tax:.2f}

Line Items:
{line_items_text}

Provide a brief summary highlighting the key details."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that summarizes invoice data concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    return response.choices[0].message.content


def generate_invoice_summary_report(
    invoice_data: Dict[str, Any], model: str = OPENAI_MODEL
) -> Dict[str, Any]:
    summary = summarize_invoice_fields(invoice_data, model)

    total = invoice_data.get("total", 0.0)
    tax = invoice_data.get("tax", 0.0)
    subtotal = invoice_data.get("subtotal", 0.0)
    line_items = invoice_data.get("line_items", [])
    item_count = len(line_items)

    return {
        "vendor_name": invoice_data.get("vendor_name", ""),
        "invoice_id": invoice_data.get("invoice_id", ""),
        "invoice_date": invoice_data.get("invoice_date", ""),
        "total": total,
        "tax": tax,
        "subtotal": subtotal,
        "item_count": item_count,
        "summary_text": summary,
        "key_metrics": {
            "total_amount": total,
            "tax_amount": tax,
            "tax_rate": (tax / subtotal * 100) if subtotal > 0 else 0.0,
            "average_item_cost": total / item_count if item_count > 0 else 0.0,
        },
    }
