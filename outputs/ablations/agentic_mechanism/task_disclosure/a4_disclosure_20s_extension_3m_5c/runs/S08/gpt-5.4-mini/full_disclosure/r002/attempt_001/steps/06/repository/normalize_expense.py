import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def _coerce_number(value: Any) -> Optional[float]:
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


def _coerce_confidence(value: Any) -> Optional[float]:
    num = _coerce_number(value)
    if num is None:
        return None
    if num < 0:
        return 0.0
    if num > 1:
        if num <= 100:
            return num / 100.0
        return 1.0
    return num


def normalize_expense(extracted_fields: Dict[str, Any], model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload = {
        "vendor": extracted_fields.get("vendor") or extracted_fields.get("merchant"),
        "date": extracted_fields.get("date") or extracted_fields.get("transaction_date"),
        "currency": extracted_fields.get("currency"),
        "total": _coerce_number(extracted_fields.get("total")),
        "tax": _coerce_number(extracted_fields.get("tax")),
        "notes": extracted_fields.get("notes") or extracted_fields.get("memo") or extracted_fields.get("description"),
        "line_items": extracted_fields.get("line_items") or extracted_fields.get("items") or [],
        "confidence": _coerce_confidence(extracted_fields.get("confidence")),
    }
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Normalize expense extraction output into a standard JSON schema with canonical keys: vendor, date, currency, total, tax, notes, line_items, confidence.",
            },
            {
                "role": "user",
                "content": str(payload),
            },
        ],
    )
    text = getattr(response, "output_text", None)
    if text:
        return {"normalized_expense": text, "provider": "openai", "model": model or DEFAULT_MODEL}
    return {"normalized_expense": payload, "provider": "openai", "model": model or DEFAULT_MODEL}
