from __future__ import annotations

from typing import Any, Dict

from document_models import ExtractedExpense, normalize_expense_record


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    expense = extracted["expense"]
    if not isinstance(expense, ExtractedExpense):
        raise TypeError("expected ExtractedExpense in extracted['expense']")
    normalized = normalize_expense_record(expense)
    normalized["source_provider"] = extracted.get(
        "provider", "azure-document-intelligence"
    )
    normalized["source_model"] = extracted.get("model_id")
    return normalized
