from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL_NAME = "gpt-4o-mini"



def invoice_summary(normalized_invoice: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "Summarize this invoice extraction for an expense reviewer in 3 concise sentences. "
        "Include vendor, date, total, and noteworthy line items.\n\n"
        f"Invoice JSON: {json.dumps(normalized_invoice, ensure_ascii=False)}"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You summarize structured invoice data clearly and accurately."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
