import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def _build_prompt(expense_fields: Dict[str, Any]) -> str:
    return (
        "Normalize the following extracted expense fields into a standard JSON schema. "
        "Return strict JSON with keys: merchant, date, currency, subtotal, tax, tip, total, items, "
        "payment_method, category, notes, confidence. "
        "Ensure amounts are numbers when possible and preserve missing values as null. "
        "Items should be a list of objects with description, quantity, unit_price, and amount when available. "
        f"Expense fields:\n\n{json.dumps(expense_fields, ensure_ascii=False)}"
    )


def _extract_output_text(data: Dict[str, Any]) -> str:
    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")
    return output_text.strip()


def _fallback_normalized(expense_fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "merchant": expense_fields.get("merchant") or expense_fields.get("vendor"),
        "date": expense_fields.get("date"),
        "currency": expense_fields.get("currency"),
        "subtotal": expense_fields.get("subtotal"),
        "tax": expense_fields.get("tax"),
        "tip": expense_fields.get("tip"),
        "total": expense_fields.get("total"),
        "items": expense_fields.get("items") or expense_fields.get("line_items") or [],
        "payment_method": expense_fields.get("payment_method"),
        "category": expense_fields.get("category"),
        "notes": expense_fields.get("notes") or expense_fields.get("memo"),
        "confidence": expense_fields.get("confidence"),
    }


def normalize_expense(expense_fields: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        return _fallback_normalized(expense_fields)

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(expense_fields),
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
    output_text = _extract_output_text(data)
    if not output_text:
        return _fallback_normalized(expense_fields)

    try:
        parsed = json.loads(output_text)
    except Exception:
        return _fallback_normalized(expense_fields)

    normalized = _fallback_normalized(expense_fields)
    normalized.update({
        "merchant": parsed.get("merchant", normalized["merchant"]),
        "date": parsed.get("date", normalized["date"]),
        "currency": parsed.get("currency", normalized["currency"]),
        "subtotal": parsed.get("subtotal", normalized["subtotal"]),
        "tax": parsed.get("tax", normalized["tax"]),
        "tip": parsed.get("tip", normalized["tip"]),
        "total": parsed.get("total", normalized["total"]),
        "items": parsed.get("items", normalized["items"]),
        "payment_method": parsed.get("payment_method", normalized["payment_method"]),
        "category": parsed.get("category", normalized["category"]),
        "notes": parsed.get("notes", normalized["notes"]),
        "confidence": parsed.get("confidence", normalized["confidence"]),
    })
    return normalized
