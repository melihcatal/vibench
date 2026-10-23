from typing import Any, Dict

from document_models import standardize_expense_record


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    return standardize_expense_record(extracted)
