from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in one paragraph: {extracted_invoice}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize extracted invoice fields."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
