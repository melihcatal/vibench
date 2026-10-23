from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

PROVIDER_NAME = "openai"
MODEL_ID = "gpt-4o-mini"


def summarize_invoice_fields(fields: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize structured invoice fields in one concise paragraph."},
            {"role": "user", "content": str(fields)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
