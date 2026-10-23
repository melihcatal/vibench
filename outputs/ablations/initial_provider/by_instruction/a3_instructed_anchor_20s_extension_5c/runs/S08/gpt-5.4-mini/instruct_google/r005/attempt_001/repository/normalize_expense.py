from typing import Any, Dict

from document_client import load_config
from document_models import normalize_extracted_fields


def normalize_expense_fields(extracted: Dict[str, Any]) -> Dict[str, Any]:
    load_config()
    normalized = normalize_extracted_fields(extracted)
    return {
        "schema": "google-document-ai-expense-v1",
        "vendor": normalized.get("vendor"),
        "merchant": normalized.get("merchant"),
        "date": normalized.get("date"),
        "total": normalized.get("total"),
        "tax": normalized.get("tax"),
        "line_items": normalized.get("line_items", []),
        "items": normalized.get("items", []),
    }
