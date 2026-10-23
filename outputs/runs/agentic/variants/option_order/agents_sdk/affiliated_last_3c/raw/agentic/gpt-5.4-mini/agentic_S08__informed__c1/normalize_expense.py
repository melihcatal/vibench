from __future__ import annotations

from typing import Any, Dict

from document_client import normalize_currency_amount
from document_models import NormalizedExpenseRecord, build_normalized_expense

PROVIDER_NAME = "azure-ai-documentintelligence"


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    record = build_normalized_expense(
        {
            "vendor": extracted.get("vendor") or extracted.get("merchant"),
            "document_date": extracted.get("date") or extracted.get("document_date"),
            "total": normalize_currency_amount(extracted.get("total")),
            "tax": normalize_currency_amount(extracted.get("tax")),
            "currency": extracted.get("currency") or "USD",
            "items": extracted.get("items", []),
            "notes": extracted.get("notes"),
            "confidence": extracted.get("confidence"),
        }
    )
    return record.to_dict()
