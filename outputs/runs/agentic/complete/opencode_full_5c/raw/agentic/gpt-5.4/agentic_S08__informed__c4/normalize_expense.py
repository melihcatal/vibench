from __future__ import annotations

from typing import Any, Dict

from document_models import normalize_expense_payload


def normalize_expense(extracted_document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = normalize_expense_payload(extracted_document)
    normalized["schema_version"] = "2026-04-19"
    normalized["record_type"] = "expense_record"
    return normalized
