import os
from typing import Any, Dict, List, Optional

import openai


def _get_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def summarize_invoice_fields(fields: Dict[str, Any]) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize extracted invoice fields clearly and concisely.",
            },
            {
                "role": "user",
                "content": f"Invoice fields: {fields}",
            },
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""


def summarize_invoice_fields_bulk(items: List[Dict[str, Any]]) -> List[str]:
    return [summarize_invoice_fields(item) for item in items]
