import os
from typing import Any, Dict, List

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def summarize_invoice_fields(fields: Dict[str, Any]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    system_prompt = (
        "You summarize extracted invoice fields into a concise, human-readable invoice summary. "
        "Return only the summary text."
    )
    user_prompt = f"Invoice fields:\n{fields}"

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def summarize_invoice_batch(invoices: List[Dict[str, Any]]) -> List[str]:
    return [summarize_invoice_fields(invoice) for invoice in invoices]
