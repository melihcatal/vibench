import argparse
import json
import os
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

import requests


OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


def _coerce_str(value):
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return str(value).strip() or None


def _coerce_decimal(value):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float, Decimal)):
        try:
            return str(Decimal(str(value)).quantize(Decimal("0.01")))
        except InvalidOperation:
            return None
    s = _coerce_str(value)
    if s is None:
        return None
    s = re.sub(r"[^0-9,.-]", "", s)
    if s.count(",") > 0 and s.count(".") == 0:
        s = s.replace(",", ".")
    elif s.count(",") > 0 and s.count(".") > 0:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    try:
        return str(Decimal(s).quantize(Decimal("0.01")))
    except InvalidOperation:
        return None


def _coerce_date(value):
    s = _coerce_str(value)
    if s is None:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def _normalize_item(item):
    if not isinstance(item, dict):
        return {
            "date": None,
            "merchant": None,
            "amount": None,
            "currency": None,
            "category": None,
            "payment_method": None,
            "tax": None,
            "tip": None,
            "notes": None,
            "source": "openai:gpt-5.4-mini",
        }
    currency = _coerce_str(item.get("currency") or item.get("ccy"))
    if currency:
        currency = currency.upper()
    return {
        "date": _coerce_date(item.get("date") or item.get("transaction_date") or item.get("expense_date")),
        "merchant": _coerce_str(item.get("merchant") or item.get("vendor") or item.get("payee")),
        "amount": _coerce_decimal(item.get("amount") or item.get("total") or item.get("value")),
        "currency": currency,
        "category": _coerce_str(item.get("category") or item.get("expense_category")),
        "payment_method": _coerce_str(item.get("payment_method") or item.get("card") or item.get("tender")),
        "tax": _coerce_decimal(item.get("tax") or item.get("vat") or item.get("sales_tax")),
        "tip": _coerce_decimal(item.get("tip") or item.get("gratuity")),
        "notes": _coerce_str(item.get("notes") or item.get("description") or item.get("memo")),
        "source": "openai:gpt-5.4-mini",
    }


def normalize_expense_fields(payload):
    if isinstance(payload, list):
        return [normalize_expense_fields(item) for item in payload]
    if isinstance(payload, dict) and any(k in payload for k in ("expenses", "items", "records")):
        key = next(k for k in ("expenses", "items", "records") if k in payload)
        return {key: [normalize_expense_fields(item) for item in payload.get(key, [])]}
    return _normalize_item(payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="Path to JSON input file; reads stdin if omitted")
    args = parser.parse_args()
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)
    else:
        payload = json.load(sys.stdin)
    result = normalize_expense_fields(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import sys

    main()
