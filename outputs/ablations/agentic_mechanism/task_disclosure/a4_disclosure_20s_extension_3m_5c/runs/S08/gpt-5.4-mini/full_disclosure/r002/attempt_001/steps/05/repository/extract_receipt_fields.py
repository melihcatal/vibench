import base64
import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def _to_data_uri(document: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{base64.b64encode(document).decode('utf-8')}"


def _normalize_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(
                {
                    "description": item.get("description") or item.get("name") or item.get("item"),
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price") or item.get("price"),
                    "amount": item.get("amount") or item.get("total"),
                }
            )
    return normalized


def extract_receipt_fields(
    document: bytes,
    mime_type: str = "image/png",
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if client is None:
        client = OpenAI(api_key=api_key)
    prompt = (
        "Extract structured receipt fields as JSON with keys: merchant, tax, total, items. "
        "Items must be a list of objects with description, quantity, unit_price, and amount when available. "
        "Return only valid JSON."
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You extract receipt fields."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _to_data_uri(document, mime_type)}},
                ],
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    return {
        "merchant": data.get("merchant"),
        "tax": data.get("tax"),
        "total": data.get("total"),
        "items": _normalize_items(data.get("items")),
    }
