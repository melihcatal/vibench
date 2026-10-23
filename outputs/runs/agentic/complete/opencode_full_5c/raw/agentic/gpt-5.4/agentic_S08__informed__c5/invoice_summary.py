from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


def summarize_invoice_fields(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Summarize extracted invoice fields into a concise finance-oriented paragraph.",
            },
            {"role": "user", "content": str(extracted_invoice)},
        ],
    )
    return response.choices[0].message.content or ""
