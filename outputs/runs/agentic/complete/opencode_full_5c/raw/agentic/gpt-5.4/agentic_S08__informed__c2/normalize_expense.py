from __future__ import annotations

from typing import Any, Dict

from document_models import build_standard_expense_schema


def normalize_expense(extracted_document: Dict[str, Any]) -> Dict[str, Any]:
    document_type = extracted_document.get("document_type", "expense")
    normalized = build_standard_expense_schema(document_type, extracted_document)
    normalized["normalization_version"] = "1.0"
    return normalized
