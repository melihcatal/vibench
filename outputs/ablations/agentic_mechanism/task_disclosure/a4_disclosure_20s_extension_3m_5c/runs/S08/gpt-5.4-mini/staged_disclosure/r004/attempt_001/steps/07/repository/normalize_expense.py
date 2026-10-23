import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _response_text(data: Dict[str, Any]) -> str:
    output = data.get("output", [])
    pieces = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    pieces.append(text)
    if pieces:
        return "".join(pieces)
    return data.get("output_text", "") or ""


def normalize_expense(expense_fields: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Normalize these extracted expense fields into this JSON schema: "
        '{"merchant": string|null, "transaction_date": string|null, "amount": number|null, '
        '"currency": string|null, "category": string|null, "payment_method": string|null, '
        '"tax_amount": number|null, "tip_amount": number|null, "confidence": number|null, '
        '"source_fields": object}. '
        "Use null when information is missing. transaction_date must be ISO 8601 date string when possible. "
        "Return only valid JSON.
        \n\n"
        f"Extracted expense fields:\n{json.dumps(expense_fields, ensure_ascii=False)}"
    )

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            }
        ],
        "temperature": 0,
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = _response_text(data).strip()
    if not text:
        raise ValueError("No structured output returned by OpenAI API")
    return json.loads(text)


__all__ = ["normalize_expense"]
