from __future__ import annotations

import os

from openai import OpenAI


def summarize_invoice_fields(extracted_invoice: dict) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize structured invoice extraction into a concise accounting review note.",
            },
            {
                "role": "user",
                "content": str(extracted_invoice),
            },
        ],
    )
    return response.output_text
