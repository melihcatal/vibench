from __future__ import annotations

from typing import Dict

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def invoice_summary(extracted_invoice: Dict[str, object]) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in one concise paragraph: {extracted_invoice}"
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize structured invoices."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
