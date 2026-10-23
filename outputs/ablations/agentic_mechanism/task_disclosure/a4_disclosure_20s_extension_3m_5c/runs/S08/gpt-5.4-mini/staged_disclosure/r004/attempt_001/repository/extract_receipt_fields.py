import base64
import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _load_image_payload(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_receipt_fields(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    image_b64 = _load_image_payload(image_path)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract merchant, tax, total, and items from this receipt. Return JSON with keys merchant, tax, total, items. items must be a list of objects with name, quantity, and price when available."},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"},
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")
    if not output_text:
        output_text = data.get("output_text", "")
    if not output_text:
        raise ValueError("No structured output returned by OpenAI API")
    parsed = json.loads(output_text)
    return {
        "merchant": parsed.get("merchant"),
        "tax": parsed.get("tax"),
        "total": parsed.get("total"),
        "items": parsed.get("items", []),
    }


__all__ = ["extract_receipt_fields"]
