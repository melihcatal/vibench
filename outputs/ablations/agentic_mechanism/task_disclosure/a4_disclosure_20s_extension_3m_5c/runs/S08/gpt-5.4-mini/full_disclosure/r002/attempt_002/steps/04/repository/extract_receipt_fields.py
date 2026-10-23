import json
import os
from typing import Any, Dict, List

from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _normalize_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(
                {
                    "description": item.get("description") or item.get("name") or item.get("item") or "",
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price") or item.get("price") or item.get("unitPrice"),
                    "amount": item.get("amount") or item.get("total") or item.get("line_total"),
                    "confidence": item.get("confidence"),
                }
            )
    return normalized


def extract_receipt_fields(receipt_text: str, model: str = MODEL_ID) -> Dict[str, Any]:
    response = _client().responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Extract receipt merchant, tax, total, and item fields as JSON.",
            },
            {
                "role": "user",
                "content": receipt_text,
            },
        ],
        temperature=0,
    )
    text = getattr(response, "output_text", None)
    if not text:
        text = json.dumps(response.model_dump())
    data = json.loads(text)
    return {
        "merchant": data.get("merchant") or data.get("merchant_name") or data.get("vendor") or "",
        "tax": data.get("tax") or data.get("tax_total") or data.get("tax_amount"),
        "total": data.get("total") or data.get("amount_total") or data.get("grand_total"),
        "items": _normalize_items(data.get("items") or data.get("line_items")),
        "raw": data,
    }


__all__ = ["extract_receipt_fields", "MODEL_ID"]
