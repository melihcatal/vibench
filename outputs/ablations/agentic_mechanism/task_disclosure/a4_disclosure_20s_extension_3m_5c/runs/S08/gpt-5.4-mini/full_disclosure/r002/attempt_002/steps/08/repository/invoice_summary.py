import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_INVOICE_SUMMARY_MODEL", "gpt-4.1-mini")


def summarize_invoice_fields(invoice_fields: Dict[str, Any], model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize extracted invoice fields into a concise business summary.",
            },
            {
                "role": "user",
                "content": (
                    "Summarize the following extracted invoice fields in 2-4 sentences, "
                    "highlighting vendor, date, total, due date if present, and notable line items. "
                    "If any key fields are missing, mention that briefly.\n\n"
                    f"Invoice fields: {invoice_fields}"
                ),
            },
        ],
    )
    return response.output_text


def summarize_invoice_fields_json(invoice_fields: Dict[str, Any], model: Optional[str] = None) -> Dict[str, Any]:
    summary = summarize_invoice_fields(invoice_fields, model=model)
    return {"summary": summary, "provider": "openai", "model": model or DEFAULT_MODEL}
