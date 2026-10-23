import json
import os
import sys
from typing import Any, Dict, List, Optional

from openai import OpenAI


MODEL = "gpt-4.1-mini"


def _coerce_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(
                {
                    "description": item.get("description") or item.get("name"),
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price"),
                    "amount": item.get("amount") or item.get("total_price"),
                    "category": item.get("category"),
                }
            )
    return normalized


def _normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "merchant": payload.get("merchant") or payload.get("vendor") or payload.get("payee"),
        "date": payload.get("date") or payload.get("transaction_date") or payload.get("expense_date"),
        "currency": payload.get("currency") or payload.get("currency_code"),
        "subtotal": payload.get("subtotal"),
        "tax": payload.get("tax") or payload.get("tax_amount"),
        "tip": payload.get("tip") or payload.get("gratuity"),
        "total": payload.get("total") or payload.get("amount") or payload.get("grand_total"),
        "payment_method": payload.get("payment_method") or payload.get("paid_by"),
        "category": payload.get("category"),
        "items": _coerce_items(payload.get("items") or payload.get("line_items")),
        "raw": payload,
    }


def normalize_expense(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "Normalize extracted expense fields into a standard JSON schema with keys merchant, date, currency, subtotal, tax, tip, total, payment_method, category, items. "
                    "items must be an array of objects with description, quantity, unit_price, amount, and category when available. "
                    "Return valid JSON only."
                ),
            },
            {"role": "user", "content": json.dumps(extracted_fields, ensure_ascii=False)},
        ],
        temperature=0,
    )
    content = response.output_text.strip()
    normalized = json.loads(content)
    if isinstance(normalized, dict):
        return _normalize_payload(normalized)
    raise RuntimeError("OpenAI response did not return a JSON object")


def main() -> None:
    extracted_fields = json.loads(sys.stdin.read() or "{}")
    result = normalize_expense(extracted_fields)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
