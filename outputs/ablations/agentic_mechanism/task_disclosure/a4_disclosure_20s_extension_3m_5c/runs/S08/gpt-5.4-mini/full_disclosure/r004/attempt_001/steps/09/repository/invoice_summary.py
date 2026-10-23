import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


def _extract_text(payload: Dict[str, Any]) -> str:
    if isinstance(payload, str):
        return payload
    if "summary" in payload and isinstance(payload["summary"], str):
        return payload["summary"]
    fields = payload.get("fields")
    if isinstance(fields, dict):
        vendor = fields.get("vendor") or fields.get("merchant") or "Unknown vendor"
        date = fields.get("date") or fields.get("invoice_date") or "Unknown date"
        total = fields.get("total") or fields.get("amount_total") or "Unknown total"
        currency = fields.get("currency")
        parts = [f"Invoice from {vendor}", f"dated {date}", f"total {total}"]
        if currency:
            parts[-1] = f"total {total} {currency}"
        return ", ".join(parts)
    return json.dumps(payload, ensure_ascii=False)


def summarize_invoice_fields(invoice_fields: Dict[str, Any], api_key: Optional[str] = None, timeout: int = 30) -> str:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Summarize the extracted invoice fields in one concise sentence. "
        "Focus on vendor, date, total, and notable line items or notes.\n\n"
        f"Input: {_extract_text(invoice_fields)}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize invoice data clearly and briefly."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("Empty response from OpenAI")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Missing summary content from OpenAI")
    return content.strip()


def build_invoice_summary(invoice_fields: Dict[str, Any]) -> Dict[str, Any]:
    summary = summarize_invoice_fields(invoice_fields)
    return {"summary": summary, "source": "openai", "model": OPENAI_MODEL}
