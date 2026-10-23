from google.cloud import documentai
from document_client import get_documentai_client, build_process_document_request
from document_models import normalize_expense

def normalize_expense(expense: dict) -> dict:
    normalized_expense = {
        "vendor": expense.get("vendor"),
        "date": expense.get("date"),
        "total": expense.get("total"),
        "items": expense.get("items")
    }
    return normalized_expense

def validate_document_fields(expense: dict) -> bool:
    required_fields = ["vendor", "date", "total", "items"]
    for field in required_fields:
        if field not in expense:
            return False
    return True