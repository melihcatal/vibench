import json
import os
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _parse_amount(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        return str(Decimal(str(value)).quantize(Decimal("0.01")))
    text = str(value).strip()
    if not text:
        return None
    cleaned = re.sub(r"[^0-9,.-]", "", text)
    if not cleaned:
        return None
    if cleaned.count(",") > 0 and cleaned.count(".") == 0:
        cleaned = cleaned.replace(",", ".")
    elif cleaned.count(",") > 0 and cleaned.count(".") > 0:
        cleaned = cleaned.replace(",", "")
    try:
        return str(Decimal(cleaned).quantize(Decimal("0.01")))
    except (InvalidOperation, ValueError):
        return None


def _parse_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    if not text:
        return None
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%b %d, %Y",
        "%B %d, %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def _normalize_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_expense(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    _ = client
    normalized = {
        "schema_version": "1.0",
        "normalized_at": datetime.now(timezone.utc).isoformat(),
        "expense": {
            "merchant": _normalize_text(extracted_fields.get("merchant") or extracted_fields.get("vendor")),
            "amount": _parse_amount(extracted_fields.get("amount") or extracted_fields.get("total")),
            "currency": _normalize_text(extracted_fields.get("currency") or extracted_fields.get("ccy")),
            "date": _parse_date(extracted_fields.get("date") or extracted_fields.get("transaction_date")),
            "category": _normalize_text(extracted_fields.get("category")),
            "payment_method": _normalize_text(extracted_fields.get("payment_method") or extracted_fields.get("card")),
            "tax": _parse_amount(extracted_fields.get("tax")),
            "tip": _parse_amount(extracted_fields.get("tip")),
            "receipt_id": _normalize_text(extracted_fields.get("receipt_id") or extracted_fields.get("id")),
            "notes": _normalize_text(extracted_fields.get("notes") or extracted_fields.get("description")),
        },
        "source_fields": extracted_fields,
        "provider": {
            "name": "openai",
            "model": OPENAI_MODEL,
        },
    }
    return normalized


def main() -> None:
    import sys

    payload = json.load(sys.stdin)
    json.dump(normalize_expense(payload), sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
