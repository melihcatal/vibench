import os
from typing import Any, Dict

from document_client import build_extract_client

OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def invoice_summary(extracted_invoice: Dict[str, Any]) -> Dict[str, Any]:
    client = build_extract_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize extracted invoice fields in concise business language as JSON."},
            {"role": "user", "content": __import__("json").dumps(extracted_invoice, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return __import__("json").loads(response.choices[0].message.content or "{}")
