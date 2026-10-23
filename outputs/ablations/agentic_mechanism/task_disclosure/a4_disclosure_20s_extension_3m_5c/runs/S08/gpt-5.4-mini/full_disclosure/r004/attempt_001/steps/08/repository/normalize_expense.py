import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _to_float(value: Any) -> Optional[float]:
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


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    quantity = _to_float(item.get("quantity"))
    unit_price = _to_float(item.get("unit_price") or item.get("unitPrice"))
    amount = _to_float(item.get("amount") or item.get("total"))
    normalized = {
        "description": item.get("description") or item.get("name") or "",
        "quantity": quantity,
        "unit_price": unit_price,
        "amount": amount,
        "currency": item.get("currency"),
        "category": item.get("category"),
    }
    return {k: v for k, v in normalized.items() if v is not None and v != ""}


def normalize_expense(expense_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = _client()
    prompt = (
        "Normalize the following extracted expense fields into this JSON schema: "
        "{vendor, transaction_date, currency, subtotal, tax, tip, total, payment_method, "
        "last4, items, notes, confidence}. Return only valid JSON. Input: "
        + json.dumps(expense_fields, ensure_ascii=False)
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
        temperature=0,
    )
    text = response.output_text.strip()
    data = json.loads(text)

    items = data.get("items") or expense_fields.get("items") or []
    normalized_items = [_normalize_item(item) for item in items if isinstance(item, dict)]

    normalized = {
        "vendor": data.get("vendor") or expense_fields.get("vendor") or expense_fields.get("merchant"),
        "transaction_date": data.get("transaction_date") or expense_fields.get("date"),
        "currency": data.get("currency") or expense_fields.get("currency"),
        "subtotal": _to_float(data.get("subtotal") or expense_fields.get("subtotal")),
        "tax": _to_float(data.get("tax") or expense_fields.get("tax")),
        "tip": _to_float(data.get("tip") or expense_fields.get("tip")),
        "total": _to_float(data.get("total") or expense_fields.get("total")),
        "payment_method": data.get("payment_method") or expense_fields.get("payment_method"),
        "last4": data.get("last4") or expense_fields.get("last4"),
        "items": normalized_items,
        "notes": data.get("notes") or expense_fields.get("notes") or expense_fields.get("memo"),
        "confidence": _to_float(data.get("confidence") or expense_fields.get("confidence")),
    }
    return {k: v for k, v in normalized.items() if v is not None and v != [] and v != ""}
