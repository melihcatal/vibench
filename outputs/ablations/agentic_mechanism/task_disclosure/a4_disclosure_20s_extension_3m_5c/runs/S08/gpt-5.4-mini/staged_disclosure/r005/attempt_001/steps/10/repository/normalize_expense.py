import json
import os
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "openai/gpt-5.4-mini"


def _to_decimal(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        try:
            return format(Decimal(str(value)).quantize(Decimal("0.01")), "f")
        except InvalidOperation:
            return None
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        cleaned = re.sub(r"[^0-9,.-]", "", text)
        if cleaned.count(",") > 0 and cleaned.count(".") == 0:
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
        try:
            return format(Decimal(cleaned).quantize(Decimal("0.01")), "f")
        except InvalidOperation:
            return None
    return None


def _normalize_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def normalize_expense(fields: Dict[str, Any]) -> Dict[str, Any]:
    vendor = fields.get("vendor") or fields.get("merchant") or fields.get("payee")
    amount = _to_decimal(fields.get("amount") or fields.get("total") or fields.get("expense_amount"))
    currency = (fields.get("currency") or fields.get("currency_code") or "USD").upper()
    date = _normalize_date(fields.get("date") or fields.get("transaction_date") or fields.get("purchase_date"))
    category = fields.get("category") or fields.get("expense_category") or "uncategorized"
    receipt_id = fields.get("receipt_id") or fields.get("id") or fields.get("document_id")

    normalized = {
        "schema_version": "1.0",
        "vendor": vendor,
        "amount": amount,
        "currency": currency,
        "date": date,
        "category": category,
        "receipt_id": receipt_id,
        "normalized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    return {k: v for k, v in normalized.items() if v is not None}


def normalize_with_openai(fields: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return normalize_expense(fields)

    prompt = (
        "Normalize these extracted expense fields into JSON with keys: "
        "schema_version, vendor, amount, currency, date, category, receipt_id, normalized_at. "
        "Use ISO date (YYYY-MM-DD), amount as a string with two decimals, and omit missing values. "
        f"Input: {json.dumps(fields, ensure_ascii=False)}"
    )
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return normalize_expense(fields)


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}
    print(json.dumps(normalize_with_openai(payload), ensure_ascii=False))
