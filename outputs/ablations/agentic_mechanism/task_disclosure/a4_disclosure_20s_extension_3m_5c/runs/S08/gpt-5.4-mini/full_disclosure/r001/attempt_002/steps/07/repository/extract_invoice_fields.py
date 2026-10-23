import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _messages(invoice_text: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Extract structured invoice fields as JSON with keys vendor, date, total, line_items. Each line item should include description, quantity, unit_price, amount, and currency when present.",
        },
        {"role": "user", "content": invoice_text},
    ]


def extract_invoice_fields(invoice_text: str) -> Dict[str, Any]:
    response = _client().responses.create(
        model=OPENAI_MODEL,
        input=_messages(invoice_text),
        temperature=0,
    )
    text = getattr(response, "output_text", None)
    if not text:
        text = response.output[0].content[0].text
    return json.loads(text)


def extract_invoice_fields_from_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return extract_invoice_fields(f.read())


__all__ = ["extract_invoice_fields", "extract_invoice_fields_from_file"]
