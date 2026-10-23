import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _standardize_items(items: Any) -> list:
    if not isinstance(items, list):
        return []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "description": item.get("description") or item.get("name") or item.get("title"),
                "quantity": _coerce_float(item.get("quantity")) or 1.0,
                "unit_price": _coerce_float(item.get("unit_price") or item.get("price")),
                "amount": _coerce_float(item.get("amount") or item.get("total")),
            }
        )
    return normalized


def _local_normalize(expense: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "currency": expense.get("currency") or expense.get("currency_code") or "USD",
        "merchant": expense.get("merchant") or expense.get("vendor") or expense.get("payee"),
        "date": expense.get("date") or expense.get("transaction_date") or expense.get("receipt_date"),
        "subtotal": _coerce_float(expense.get("subtotal")),
        "tax": _coerce_float(expense.get("tax") or expense.get("tax_amount")),
        "tip": _coerce_float(expense.get("tip") or expense.get("gratuity")),
        "total": _coerce_float(expense.get("total") or expense.get("amount") or expense.get("grand_total")),
        "notes": expense.get("notes") or expense.get("memo") or expense.get("description"),
        "items": _standardize_items(expense.get("items") or expense.get("line_items")),
    }


def _remote_normalize(expense: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for remote normalization")

    schema = {
        "name": "expense_normalization",
        "schema": {
            "type": "object",
            "properties": {
                "provider": {"type": "string"},
                "model": {"type": "string"},
                "currency": {"type": ["string", "null"]},
                "merchant": {"type": ["string", "null"]},
                "date": {"type": ["string", "null"]},
                "subtotal": {"type": ["number", "null"]},
                "tax": {"type": ["number", "null"]},
                "tip": {"type": ["number", "null"]},
                "total": {"type": ["number", "null"]},
                "notes": {"type": ["string", "null"]},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": ["string", "null"]},
                            "quantity": {"type": ["number", "null"]},
                            "unit_price": {"type": ["number", "null"]},
                            "amount": {"type": ["number", "null"]},
                        },
                        "required": ["description", "quantity", "unit_price", "amount"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["provider", "model", "currency", "merchant", "date", "subtotal", "tax", "tip", "total", "notes", "items"],
            "additionalProperties": False,
        },
    }

    response = requests.post(
        f"{OPENAI_API_BASE}/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": "Normalize expense extraction into a standard JSON schema.",
                },
                {
                    "role": "user",
                    "content": json.dumps(expense, ensure_ascii=False),
                },
            ],
            "response_format": {"type": "json_schema", "json_schema": schema},
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data.get("output_text")
    if text:
        return json.loads(text)
    output = data.get("output", [])
    for item in output:
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return json.loads(content.get("text", "{}"))
    raise RuntimeError("OpenAI normalization response did not contain JSON output")


def normalize_expense(expense: Dict[str, Any], use_remote: bool = False) -> Dict[str, Any]:
    if use_remote:
        return _remote_normalize(expense)
    return _local_normalize(expense)
