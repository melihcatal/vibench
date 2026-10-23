import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def _build_prompt(receipt_text: str) -> str:
    return (
        "Extract structured receipt fields from the following receipt text. "
        "Return strict JSON with keys: merchant, tax, total, items. "
        "Each item should include description, quantity, unit_price, and amount when available. "
        "If a value is missing, use null. Receipt text:\n\n"
        f"{receipt_text}"
    )


def extract_receipt_fields(receipt_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(receipt_text),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text:
        return {"merchant": None, "tax": None, "total": None, "items": []}

    try:
        import json

        parsed = json.loads(output_text)
    except Exception:
        return {"merchant": None, "tax": None, "total": None, "items": []}

    return {
        "merchant": parsed.get("merchant"),
        "tax": parsed.get("tax"),
        "total": parsed.get("total"),
        "items": parsed.get("items", []),
    }
