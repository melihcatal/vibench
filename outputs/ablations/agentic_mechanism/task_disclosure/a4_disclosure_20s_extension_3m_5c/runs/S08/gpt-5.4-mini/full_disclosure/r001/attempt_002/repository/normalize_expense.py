import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _prompt(expense_data: Dict[str, Any]) -> str:
    return (
        "Normalize extracted expense fields into a standard JSON schema with keys "
        "vendor, transaction_date, currency, subtotal, tax, total, payment_method, notes, line_items, and source. "
        "Preserve available values, convert dates to ISO 8601 when possible, represent missing values as null, "
        "and ensure line_items is a list of objects with description, quantity, unit_price, amount, and currency when present. "
        "Return valid JSON only. Expense data:\n"
        f"{json.dumps(expense_data, ensure_ascii=False)}"
    )


def normalize_expense(expense_data: Dict[str, Any]) -> Dict[str, Any]:
    response = _client().responses.create(
        model=MODEL_ID,
        input=_prompt(expense_data),
        temperature=0,
    )
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = ""
        for item in getattr(response, "output", []):
            for content in getattr(item, "content", []):
                text = getattr(content, "text", None)
                if text:
                    output_text += text
    return json.loads(output_text)


def normalize_expense_from_json(expense_json: str) -> Dict[str, Any]:
    return normalize_expense(json.loads(expense_json))


__all__ = ["normalize_expense", "normalize_expense_from_json"]
