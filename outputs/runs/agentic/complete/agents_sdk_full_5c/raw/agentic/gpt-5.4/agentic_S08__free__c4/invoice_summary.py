from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def invoice_summary(invoice_data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize extracted invoice fields into a concise finance-review summary.",
            },
            {"role": "user", "content": str(invoice_data)},
        ],
    )
    return completion.choices[0].message.content or ""
