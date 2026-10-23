import os
from typing import Any, Dict, Optional

from document_client import build_extract_client
from document_models import normalize_expense_record

OPENAI_MODEL = os.getenv("OPENAI_EXPENSE_NORMALIZATION_MODEL", "gpt-4o-mini")


def normalize_expense(extracted_fields: Dict[str, Any], source: Optional[str] = None) -> Dict[str, Any]:
    client = build_extract_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Normalize extracted expense data into a standard JSON schema with vendor, transaction_date, total_amount, currency, tax_amount, items, notes, and confidence.",
            },
            {
                "role": "user",
                "content": normalize_expense_record(extracted_fields, source=source),
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return response.choices[0].message.parsed if hasattr(response.choices[0].message, "parsed") and response.choices[0].message.parsed else __import__("json").loads(response.choices[0].message.content or "{}")


if __name__ == "__main__":
    raise SystemExit(0)
