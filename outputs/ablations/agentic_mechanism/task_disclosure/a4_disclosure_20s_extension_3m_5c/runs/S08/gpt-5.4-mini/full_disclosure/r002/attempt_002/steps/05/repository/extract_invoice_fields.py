import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(
                {
                    "description": item.get("description") or item.get("name") or "",
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price") or item.get("price"),
                    "amount": item.get("amount") or item.get("total"),
                    "confidence": item.get("confidence"),
                }
            )
    return normalized


def extract_invoice_fields(invoice_text: str, model: str = MODEL_ID) -> Dict[str, Any]:
    response = _client().responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Extract invoice vendor, date, total, and line-item fields as JSON.",
            },
            {
                "role": "user",
                "content": invoice_text,
            },
        ],
        temperature=0,
    )
    text = getattr(response, "output_text", None)
    if not text:
        text = json.dumps(response.model_dump())
    data = json.loads(text)
    return {
        "vendor": data.get("vendor") or data.get("vendor_name") or "",
        "date": data.get("date") or data.get("invoice_date") or "",
        "total": data.get("total") or data.get("amount_total") or data.get("grand_total"),
        "line_items": _normalize_line_items(data.get("line_items") or data.get("items")),
        "raw": data,
    }


__all__ = ["extract_invoice_fields", "MODEL_ID"]
