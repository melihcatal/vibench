import base64
import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def _to_data_uri(image_bytes: bytes, mime_type: str = "image/png") -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"


def _normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized.append({
                "description": item.get("description") or item.get("name") or item.get("item"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("unit_price") or item.get("price"),
                "amount": item.get("amount") or item.get("total"),
            })
    return normalized


def extract_invoice_fields(document: bytes, mime_type: str = "image/png", client: Optional[OpenAI] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if client is None:
        client = OpenAI(api_key=api_key)
    prompt = (
        "Extract structured invoice fields as JSON with keys: vendor, date, total, line_items. "
        "Line items must be a list of objects with description, quantity, unit_price, and amount when available. "
        "Return only valid JSON."
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You extract invoice fields."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": _to_data_uri(document, mime_type)}},
            ]},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    return {
        "vendor": data.get("vendor"),
        "date": data.get("date"),
        "total": data.get("total"),
        "line_items": _normalize_line_items(data.get("line_items")),
    }
