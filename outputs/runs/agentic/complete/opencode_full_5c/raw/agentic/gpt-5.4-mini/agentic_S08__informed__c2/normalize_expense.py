from typing import Any, Dict

from document_models import ExpenseNormalizationRequest, standardize_expense_record


def normalize_expense(request: ExpenseNormalizationRequest) -> Dict[str, Any]:
    return standardize_expense_record(request.raw_fields)
