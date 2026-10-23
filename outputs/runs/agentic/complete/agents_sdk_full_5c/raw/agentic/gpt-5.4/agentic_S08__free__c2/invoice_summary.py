from __future__ import annotations

import os

from openai import OpenAI


MODEL = "gpt-4o-mini"
OPENAI_ENV = "OPENAI_API_KEY"


def invoice_summary(normalized_expense: dict) -> str:
    client = OpenAI(api_key=os.environ.get(OPENAI_ENV))
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize invoice fields for an accounts payable operator in 2-4 concise sentences.",
            },
            {
                "role": "user",
                "content": str(normalized_expense),
            },
        ],
    )
    return response.output_text
