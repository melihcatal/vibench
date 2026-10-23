from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        if text.endswith("```"):
            text = text[:-3]
    return text.strip()


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        try:
            return int(float(cleaned))
        except ValueError:
            return None
    return None


def _parse_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "description": item.get("description") or item.get("name") or item.get("text"),
                "quantity": _coerce_float(item.get("quantity")),
                "unit_price": _coerce_float(item.get("unit_price") or item.get("price") or item.get("amount")),
                "total": _coerce_float(item.get("total") or item.get("line_total") or item.get("amount")),
            }
        )
    return normalized


def _local_normalize(expense: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "normalized_at": datetime.now(timezone.utc).isoformat(),
        "currency": expense.get("currency") or expense.get("transaction_currency"),
        "vendor": expense.get("vendor") or expense.get("merchant") or expense.get("payee"),
        "date": expense.get("date") or expense.get("transaction_date") or expense.get("receipt_date"),
        "subtotal": _coerce_float(expense.get("subtotal")),
        "tax": _coerce_float(expense.get("tax") or expense.get("tax_amount")),
        "tip": _coerce_float(expense.get("tip")),
        "total": _coerce_float(expense.get("total") or expense.get("grand_total") or expense.get("amount")),
        "notes": expense.get("notes") or expense.get("memo") or expense.get("description"),
        "items": _parse_items(expense.get("items") or expense.get("line_items")),
        "confidence": _coerce_float(expense.get("confidence")),
        "source": expense,
    }
    return normalized


def normalize_expense(expense: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _local_normalize(expense)

    prompt = {
        "role": "user",
        "content": (
            "Normalize this extracted expense into strict JSON with keys: "
            "provider, model, normalized_at, currency, vendor, date, subtotal, tax, tip, total, notes, items, confidence. "
            "Items must be an array of objects with description, quantity, unit_price, total. "
            "Return only valid JSON. Input: " + json.dumps(expense, ensure_ascii=False)
        ),
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [prompt],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return json.loads(_strip_code_fences(content))
