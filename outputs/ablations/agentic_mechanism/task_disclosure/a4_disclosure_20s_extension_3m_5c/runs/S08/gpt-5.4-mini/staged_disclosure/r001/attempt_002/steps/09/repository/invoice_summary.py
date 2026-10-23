import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_invoice_fields(extracted_fields: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

    prompt = (
        "Summarize these extracted invoice fields in a concise, human-readable paragraph. "
        "Highlight vendor, invoice number, date, total, due date, and any notable missing or inconsistent fields. "
        f"Fields: {extracted_fields}"
    )

    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text.strip()


def summarize_invoice_fields_batch(extracted_invoices: List[Dict[str, Any]]) -> List[str]:
    return [summarize_invoice_fields(invoice) for invoice in extracted_invoices]
