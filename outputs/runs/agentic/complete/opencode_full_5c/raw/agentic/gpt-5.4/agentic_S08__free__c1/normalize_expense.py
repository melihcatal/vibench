from __future__ import annotations

from typing import Any, Dict

from document_models import to_standard_expense_schema


NORMALIZER_PROVIDER = "google_document_ai"


def normalize_expense(extraction_result: Dict[str, Any]) -> Dict[str, Any]:
    normalized = to_standard_expense_schema(extraction_result)
    normalized["normalizer"] = NORMALIZER_PROVIDER
    normalized["source_model"] = "google-cloud-documentai"
    return normalized
