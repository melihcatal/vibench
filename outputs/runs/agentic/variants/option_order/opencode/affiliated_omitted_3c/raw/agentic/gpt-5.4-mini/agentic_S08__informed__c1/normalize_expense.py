from typing import Any, Dict
from document_client import confidence_score, normalize_text
from document_models import normalize_expense_record


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_expense_record(extracted, normalize_text, confidence_score)
