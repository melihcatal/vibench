from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from document_client import get_openai_client


OPENAI_MODEL = "gpt-4.1-mini"


def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Summarize extracted invoice fields for accounts payable staff in 3 concise sentences."},
            {"role": "user", "content": str(extracted_invoice)},
        ],
    )
    return response.choices[0].message.content or ""
