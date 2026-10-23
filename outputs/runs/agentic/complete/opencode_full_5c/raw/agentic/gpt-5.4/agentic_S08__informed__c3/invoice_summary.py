from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI


def summarize_invoice_fields(normalized_record: Dict) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize structured invoice data into a concise finance-oriented summary.",
            },
            {"role": "user", "content": str(normalized_record)},
        ],
    )
    return response.choices[0].message.content or ""
