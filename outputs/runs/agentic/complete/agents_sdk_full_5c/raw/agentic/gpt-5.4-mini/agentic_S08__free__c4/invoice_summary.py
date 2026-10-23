from __future__ import annotations

from openai import OpenAI

SUMMARY_MODEL = "gpt-4.1-mini"


def invoice_summary(invoice_fields: dict) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=SUMMARY_MODEL,
        input=[
            {"role": "system", "content": "Summarize extracted invoice fields in one concise paragraph."},
            {"role": "user", "content": str(invoice_fields)},
        ],
    )
    return response.output_text
