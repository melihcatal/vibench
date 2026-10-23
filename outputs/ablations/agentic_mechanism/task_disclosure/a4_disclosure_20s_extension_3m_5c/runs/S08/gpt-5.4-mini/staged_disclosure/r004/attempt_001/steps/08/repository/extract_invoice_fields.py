import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _text_from_response(data: Dict[str, Any]) -> str:
    output = data.get("output", [])
    parts = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    parts.append(text)
    if parts:
        return "".join(parts)
    return data.get("output_text", "") or ""


def extract_invoice_fields(invoice_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Extract vendor, date, total, and line-item fields from the invoice text. "
        "Return only valid JSON with keys vendor, date, total, and line_items. "
        "line_items must be an array of objects with fields description, quantity, unit_price, and amount. "
        "If a field is missing, use null for scalar fields and [] for line_items.\n\n"
        f"Invoice text:\n{invoice_text}"
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
    text = _text_from_response(data).strip()
    if not text:
        raise ValueError("Empty response from OpenAI API")
    return json.loads(text)
