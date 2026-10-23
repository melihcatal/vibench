from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI



def summarize_invoice_fields(extracted_invoice: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize structured invoice fields into a concise accounting note.",
            },
            {
                "role": "user",
                "content": str(extracted_invoice),
            },
        ],
        max_output_tokens=180,
    )
    return response.output_text
