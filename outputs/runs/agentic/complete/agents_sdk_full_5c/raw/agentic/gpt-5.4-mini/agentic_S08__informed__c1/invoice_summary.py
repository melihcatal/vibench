from __future__ import annotations

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def invoice_summary(extracted_invoice_text: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize invoice extraction results succinctly."},
            {"role": "user", "content": extracted_invoice_text},
        ],
    )
    return completion.choices[0].message.content or ""
