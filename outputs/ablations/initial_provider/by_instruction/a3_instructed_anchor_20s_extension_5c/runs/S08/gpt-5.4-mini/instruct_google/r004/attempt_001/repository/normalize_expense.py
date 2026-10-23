import json
from typing import Any, Dict

from document_models import standard_expense_schema


def normalize_expense(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = standard_expense_schema(payload)
    normalized["provider"] = "google-cloud-documentai"
    return normalized
