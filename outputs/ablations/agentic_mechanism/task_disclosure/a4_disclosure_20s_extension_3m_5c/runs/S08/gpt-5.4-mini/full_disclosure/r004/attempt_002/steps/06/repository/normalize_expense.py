import json
import os
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_EXPENSE_NORMALIZER_MODEL", "gpt-4.1-mini")


def _to_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    return str(value).strip() or None


def _to_decimal(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    try:
        return format(Decimal(str(value)), "f")
    except (InvalidOperation, ValueError, TypeError):
        return None


def _to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "description": _to_str(item.get("description") or item.get("name") or item.get("item")),
        "quantity": _to_float(item.get("quantity") or item.get("qty")),
        "unit_price": _to_decimal(item.get("unit_price") or item.get("price") or item.get("unitPrice")),
        "amount": _to_decimal(item.get("amount") or item.get("total") or item.get("line_total")),
        "category": _to_str(item.get("category")),
    }


def normalize_expense_fields(extracted: Dict[str, Any]) -> Dict[str, Any]:
    items = extracted.get("items") or extracted.get("line_items") or []
    normalized_items = [
        _normalize_item(item)
        for item in items
        if isinstance(item, dict)
    ]
    total = _to_decimal(extracted.get("total") or extracted.get("grand_total") or extracted.get("amount_total"))
    tax = _to_decimal(extracted.get("tax") or extracted.get("sales_tax") or extracted.get("vat"))
    return {
        "schema_version": "1.0",
        "source": _to_str(extracted.get("source") or extracted.get("document_type") or "expense_document"),
        "merchant": _to_str(extracted.get("merchant") or extracted.get("vendor") or extracted.get("payee")),
        "transaction_date": _to_str(extracted.get("date") or extracted.get("transaction_date") or extracted.get("purchase_date")),
        "currency": _to_str(extracted.get("currency") or extracted.get("currency_code")),
        "subtotal": _to_decimal(extracted.get("subtotal") or extracted.get("net_total") or extracted.get("pre_tax_total")),
        "tax": tax,
        "total": total,
        "payment_method": _to_str(extracted.get("payment_method") or extracted.get("tender_type")),
        "invoice_number": _to_str(extracted.get("invoice_number") or extracted.get("receipt_number") or extracted.get("document_number")),
        "notes": _to_str(extracted.get("notes") or extracted.get("memo") or extracted.get("description")),
        "items": normalized_items,
        "confidence": {
            "merchant": _to_float((extracted.get("confidence") or {}).get("merchant") if isinstance(extracted.get("confidence"), dict) else extracted.get("merchant_confidence")),
            "transaction_date": _to_float((extracted.get("confidence") or {}).get("transaction_date") if isinstance(extracted.get("confidence"), dict) else extracted.get("date_confidence")),
            "total": _to_float((extracted.get("confidence") or {}).get("total") if isinstance(extracted.get("confidence"), dict) else extracted.get("total_confidence")),
        },
        "normalized_at": datetime.now(timezone.utc).isoformat(),
    }


def normalize_expense_with_openai(extracted: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    prompt = {
        "role": "user",
        "content": json.dumps(
            {
                "task": "Normalize extracted expense fields into a standard JSON schema.",
                "schema": {
                    "schema_version": "1.0",
                    "source": "string",
                    "merchant": "string|null",
                    "transaction_date": "string|null",
                    "currency": "string|null",
                    "subtotal": "string|null",
                    "tax": "string|null",
                    "total": "string|null",
                    "payment_method": "string|null",
                    "invoice_number": "string|null",
                    "notes": "string|null",
                    "items": [
                        {
                            "description": "string|null",
                            "quantity": "number|null",
                            "unit_price": "string|null",
                            "amount": "string|null",
                            "category": "string|null",
                        }
                    ],
                    "confidence": {
                        "merchant": "number|null",
                        "transaction_date": "number|null",
                        "total": "number|null",
                    },
                    "normalized_at": "string",
                },
                "input": extracted,
            }
        ),
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[prompt],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text)


__all__ = ["normalize_expense_fields", "normalize_expense_with_openai", "OPENAI_MODEL"]
