from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4.1-mini"


def invoice_summary(invoice_fields: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in one concise paragraph: {invoice_fields}"
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
