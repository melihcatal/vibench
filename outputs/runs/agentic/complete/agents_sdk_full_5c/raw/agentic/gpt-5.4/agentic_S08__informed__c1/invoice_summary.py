from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL = "gpt-4o-mini"



def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize this extracted invoice for an accounts payable reviewer in 4 concise bullet points. "
        "Include vendor, invoice date, total, and any notable line items.\n\n"
        f"Invoice JSON:\n{json.dumps(extracted_invoice, ensure_ascii=False)}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You summarize structured invoice data accurately."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
