from typing import Any, Dict

from document_models import normalize_expense_record


def normalize_expense(payload: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_expense_record(payload)
