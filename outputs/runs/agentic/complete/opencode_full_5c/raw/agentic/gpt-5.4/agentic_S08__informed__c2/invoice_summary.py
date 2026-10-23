from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def summarize_invoice_fields(normalized_invoice: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize invoice extraction output into a concise accounting-ready summary.",
            },
            {
                "role": "user",
                "content": str(normalized_invoice),
            },
        ],
    )
    return response.output_text
