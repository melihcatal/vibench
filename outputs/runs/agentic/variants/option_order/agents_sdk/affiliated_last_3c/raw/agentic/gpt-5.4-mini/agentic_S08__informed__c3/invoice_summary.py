from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in 2-3 sentences:\n{extracted_invoice}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
