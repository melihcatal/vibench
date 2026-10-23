from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


def invoice_summary(extracted_invoice: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "vendor": extracted_invoice.get("vendor"),
        "invoice_date": extracted_invoice.get("invoice_date"),
        "total": extracted_invoice.get("total"),
        "line_items": extracted_invoice.get("line_items", []),
        "notes": extracted_invoice.get("notes"),
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize invoice extraction results in concise business language.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
