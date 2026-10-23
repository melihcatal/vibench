import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _safe_json_loads(text: str) -> Dict[str, Any]:
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except Exception:
        pass
    return {}


def _normalize_items(items: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not isinstance(items, list):
        return normalized
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "description": item.get("description") or item.get("name") or "",
                "quantity": item.get("quantity") or item.get("qty") or 1,
                "unit_price": item.get("unit_price") or item.get("price") or item.get("amount"),
                "amount": item.get("amount") or item.get("total"),
                "currency": item.get("currency") or item.get("currency_code"),
            }
        )
    return normalized


def _fallback_normalize(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": payload.get("vendor") or payload.get("merchant") or payload.get("supplier") or "",
        "date": payload.get("date") or payload.get("invoice_date") or payload.get("transaction_date") or "",
        "total": payload.get("total") or payload.get("amount_total") or payload.get("grand_total"),
        "tax": payload.get("tax") or payload.get("tax_total") or payload.get("vat"),
        "currency": payload.get("currency") or payload.get("currency_code") or "",
        "items": _normalize_items(payload.get("items") or payload.get("line_items") or []),
        "notes": payload.get("notes") or payload.get("memo") or payload.get("description") or "",
        "confidence": payload.get("confidence"),
    }


def normalize_expense(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    prompt = (
        "Normalize extracted expense fields into this JSON schema: "
        '{"vendor":string,"date":string,"total":number|null,"tax":number|null,'
        '"currency":string,"items":[{"description":string,"quantity":number,"unit_price":number|null,"amount":number|null,"currency":string|null}],'
        '"notes":string,"confidence":number|null}. '
        "Return only valid JSON. Source fields: "
        + json.dumps(extracted_fields, ensure_ascii=False)
    )
    try:
        response = _client().responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )
        text = getattr(response, "output_text", None)
        if not text:
            return _fallback_normalize(extracted_fields)
        normalized = _safe_json_loads(text)
        if normalized:
            normalized.setdefault("items", [])
            normalized["items"] = _normalize_items(normalized.get("items"))
            return normalized
    except Exception:
        pass
    return _fallback_normalize(extracted_fields)


def normalize_expense_from_json(raw_json: str) -> Dict[str, Any]:
    data = _safe_json_loads(raw_json)
    return normalize_expense(data)
