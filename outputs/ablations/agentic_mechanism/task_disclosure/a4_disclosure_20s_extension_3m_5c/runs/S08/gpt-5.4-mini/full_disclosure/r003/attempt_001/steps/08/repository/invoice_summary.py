from __future__ import annotations

import os
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def summarize_invoice_fields(invoice_fields: Mapping[str, Any], model: Optional[str] = None) -> Dict[str, Any]:
    client = _client()
    model_name = model or os.environ.get("OPENAI_MODEL", "openai/gpt-5.4-mini")
    schema = {
        "name": "invoice_summary",
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
            },
            "required": ["summary"],
            "additionalProperties": False,
        },
        "strict": True,
    }
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "Summarize extracted invoice fields into a concise natural-language summary.",
            },
            {"role": "user", "content": str(dict(invoice_fields))},
        ],
        text={"format": {"type": "json_schema", "json_schema": schema}},
    )
    return response.output_parsed  # type: ignore[attr-defined]


def summarize_invoice_fields_from_text(invoice_fields: Mapping[str, Any]) -> Dict[str, Any]:
    return summarize_invoice_fields(invoice_fields)
