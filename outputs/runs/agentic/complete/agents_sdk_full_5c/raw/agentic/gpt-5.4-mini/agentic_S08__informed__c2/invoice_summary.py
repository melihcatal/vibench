from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def invoice_summary(invoice_fields: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in 3 concise bullets: {invoice_fields}"
    response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""
