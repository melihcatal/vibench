import json
import os
from typing import Any, Dict, List, Mapping, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _messages(invoice_fields: Mapping[str, Any]) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Summarize extracted invoice fields into concise JSON with keys summary, key_points, and payment_status. Keep the summary brief and preserve important amounts, vendors, dates, and line-item context.",
        },
        {"role": "user", "content": json.dumps(dict(invoice_fields), ensure_ascii=False)},
    ]


def summarize_invoice_fields(invoice_fields: Mapping[str, Any]) -> Dict[str, Any]:
    response = _client().responses.create(
        model=OPENAI_MODEL,
        input=_messages(invoice_fields),
        temperature=0,
    )
    text = getattr(response, "output_text", None)
    if not text:
        text = response.output[0].content[0].text
    return json.loads(text)


def summarize_invoice_fields_from_json(payload: str) -> Dict[str, Any]:
    return summarize_invoice_fields(json.loads(payload))


__all__ = ["summarize_invoice_fields", "summarize_invoice_fields_from_json"]
