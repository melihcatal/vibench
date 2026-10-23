from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize invoice fields into a concise business summary with vendor, date, total, and notable line items.",
            },
            {"role": "user", "content": str(extracted_invoice)},
        ],
    )
    return response.choices[0].message.content or ""
