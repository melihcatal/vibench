import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def _build_prompt(invoice_fields: Dict[str, Any]) -> str:
    return (
        "Summarize the following extracted invoice fields into a concise JSON object. "
        "Return strict JSON with keys: summary, vendor, date, total, line_item_count, highlights. "
        "The summary should be one short sentence describing the invoice. "
        "Highlights should be a list of short bullet-like strings about notable invoice details. "
        f"Invoice fields:\n\n{json.dumps(invoice_fields, ensure_ascii=False)}"
    )


def _extract_output_text(data: Dict[str, Any]) -> str:
    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")
    return output_text.strip()


def _fallback_summary(invoice_fields: Dict[str, Any]) -> Dict[str, Any]:
    line_items = invoice_fields.get("line_items") or []
    vendor = invoice_fields.get("vendor")
    date = invoice_fields.get("date")
    total = invoice_fields.get("total")
    summary_parts = []
    if vendor:
        summary_parts.append(f"Invoice from {vendor}")
    else:
        summary_parts.append("Invoice")
    if date:
        summary_parts.append(f"dated {date}")
    if total is not None:
        summary_parts.append(f"for total {total}")
    summary = " ".join(summary_parts)
    return {
        "summary": summary.strip(),
        "vendor": vendor,
        "date": date,
        "total": total,
        "line_item_count": len(line_items) if isinstance(line_items, list) else 0,
        "highlights": [],
    }


def invoice_summary(invoice_fields: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        return _fallback_summary(invoice_fields)

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(invoice_fields),
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
        return _fallback_summary(invoice_fields)

    try:
        parsed = json.loads(output_text)
    except Exception:
        return _fallback_summary(invoice_fields)

    fallback = _fallback_summary(invoice_fields)
    return {
        "summary": parsed.get("summary", fallback["summary"]),
        "vendor": parsed.get("vendor", fallback["vendor"]),
        "date": parsed.get("date", fallback["date"]),
        "total": parsed.get("total", fallback["total"]),
        "line_item_count": parsed.get("line_item_count", fallback["line_item_count"]),
        "highlights": parsed.get("highlights", fallback["highlights"]),
    }
