import json
import os
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _coerce_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _format_currency(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, (int, float)):
        return f"{value:.2f}" if isinstance(value, float) else str(value)
    return str(value)


def _join_nonempty(parts: Iterable[str]) -> str:
    return " ".join(part for part in parts if part)


def summarize_invoice_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    vendor = str(extracted_fields.get("vendor", "")).strip() or "Unknown vendor"
    invoice_date = str(extracted_fields.get("date", "")).strip() or "unknown date"
    total = _format_currency(extracted_fields.get("total"))
    currency = str(extracted_fields.get("currency", "")).strip()
    line_items = extracted_fields.get("line_items") or []
    item_count = len(line_items) if isinstance(line_items, list) else 0

    summary_parts = [
        f"Invoice from {vendor}",
        f"dated {invoice_date}",
        f"totaling {total}",
    ]
    if currency:
        summary_parts.append(currency)
    summary_parts.append(f"with {item_count} line item{'s' if item_count != 1 else ''}")

    summary = _join_nonempty(summary_parts)

    key_fields = {
        "vendor": vendor,
        "date": invoice_date,
        "total": total,
        "currency": currency or None,
        "line_item_count": item_count,
    }
    return {"summary": summary, "key_fields": key_fields}


def summarize_invoice_fields_with_openai(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Summarize extracted invoice fields concisely as strict JSON with keys summary and key_fields.",
            },
            {"role": "user", "content": json.dumps(_coerce_mapping(extracted_fields), ensure_ascii=False)},
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)
