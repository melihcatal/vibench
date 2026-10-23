from typing import Any, Dict

from document_models import normalize_expense_payload


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    payload = normalize_expense_payload(extracted)
    payload["source"] = "azure-document-intelligence"
    return payload
