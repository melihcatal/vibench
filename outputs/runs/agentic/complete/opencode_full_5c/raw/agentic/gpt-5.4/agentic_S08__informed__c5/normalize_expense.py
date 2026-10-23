from __future__ import annotations

from typing import Any, Dict

from document_models import normalize_expense_record


def normalize_expense(extracted_document: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_expense_record(extracted_document)
