from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL = "gpt-4o-mini"


def summarize_invoice_fields(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize structured invoice data into a concise accounting-ready paragraph.",
            },
            {
                "role": "user",
                "content": json.dumps(extracted_invoice, ensure_ascii=False),
            },
        ],
    )
    return response.choices[0].message.content or ""
