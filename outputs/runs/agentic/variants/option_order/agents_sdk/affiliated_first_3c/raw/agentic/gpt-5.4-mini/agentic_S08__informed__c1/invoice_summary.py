from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize invoice data concisely."},
            {"role": "user", "content": str(extracted_invoice)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
