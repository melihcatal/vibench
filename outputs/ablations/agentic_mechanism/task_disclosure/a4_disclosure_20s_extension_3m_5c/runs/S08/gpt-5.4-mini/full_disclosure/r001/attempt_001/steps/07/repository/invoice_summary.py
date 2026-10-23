import os
from typing import Any, Dict, Optional

from openai import OpenAI


def summarize_invoice_fields(invoice_fields: Dict[str, Any], model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = model or "gpt-5.4-mini"
    prompt = (
        "Summarize the following extracted invoice fields into a concise business summary. "
        "Include vendor, date, total, and notable line items if present. Return plain text only.\n\n"
        f"Invoice fields: {invoice_fields}"
    )
    response = client.responses.create(
        model=model_name,
        input=prompt,
    )
    return response.output_text
