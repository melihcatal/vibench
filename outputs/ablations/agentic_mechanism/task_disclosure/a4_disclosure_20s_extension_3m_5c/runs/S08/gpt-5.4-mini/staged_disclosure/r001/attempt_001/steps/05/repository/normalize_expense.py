import json
import os
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


STANDARD_SCHEMA = {
    "type": "object",
    "properties": {
        "merchant_name": {"type": ["string", "null"]},
        "transaction_date": {"type": ["string", "null"]},
        "currency": {"type": ["string", "null"]},
        "total_amount": {"type": ["number", "null"]},
        "tip_amount": {"type": ["number", "null"]},
        "tax_amount": {"type": ["number", "null"]},
        "category": {"type": ["string", "null"]},
        "payment_method": {"type": ["string", "null"]},
        "receipt_id": {"type": ["string", "null"]},
        "confidence": {"type": ["number", "null"]},
    },
    "required": [
        "merchant_name",
        "transaction_date",
        "currency",
        "total_amount",
        "tip_amount",
        "tax_amount",
        "category",
        "payment_method",
        "receipt_id",
        "confidence",
    ],
    "additionalProperties": False,
}


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            return None
        try:
            return Decimal(text)
        except InvalidOperation:
            return None
    return None


def _normalize_number(value: Any) -> Optional[float]:
    number = _to_decimal(value)
    return float(number) if number is not None else None


def _first_present(data: Dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def normalize_expense(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        "merchant_name": _first_present(extracted_fields, ["merchant_name", "merchant", "vendor", "store_name"]),
        "transaction_date": _first_present(extracted_fields, ["transaction_date", "date", "purchase_date"]),
        "currency": _first_present(extracted_fields, ["currency", "ccy"]),
        "total_amount": _normalize_number(_first_present(extracted_fields, ["total_amount", "amount", "total", "grand_total"])),
        "tip_amount": _normalize_number(_first_present(extracted_fields, ["tip_amount", "tip"])),
        "tax_amount": _normalize_number(_first_present(extracted_fields, ["tax_amount", "tax"])),
        "category": _first_present(extracted_fields, ["category", "expense_category"]),
        "payment_method": _first_present(extracted_fields, ["payment_method", "card_type", "payment_type"]),
        "receipt_id": _first_present(extracted_fields, ["receipt_id", "transaction_id", "id"]),
        "confidence": _normalize_number(_first_present(extracted_fields, ["confidence", "score"])),
    }
    return normalized


def normalize_with_openai(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Normalize extracted expense fields into the requested JSON schema exactly.",
            },
            {
                "role": "user",
                "content": json.dumps(extracted_fields),
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "expense_normalization",
                "schema": STANDARD_SCHEMA,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


def main() -> None:
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    result = normalize_with_openai(payload) if os.environ.get("OPENAI_API_KEY") else normalize_expense(payload)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
