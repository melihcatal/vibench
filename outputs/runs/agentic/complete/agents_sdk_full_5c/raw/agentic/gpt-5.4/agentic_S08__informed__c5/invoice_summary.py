from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


def invoice_summary(extracted_invoice: Dict[str, Any], model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Summarize invoice fields into concise finance-ready JSON with keys summary, risks, and payment_observation.",
            },
            {
                "role": "user",
                "content": json.dumps(extracted_invoice, ensure_ascii=False),
            },
        ],
    )
    return response.choices[0].message.content or "{}"
