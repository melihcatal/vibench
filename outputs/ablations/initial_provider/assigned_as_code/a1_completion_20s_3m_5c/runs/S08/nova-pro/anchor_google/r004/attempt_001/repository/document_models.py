from typing import Dict, List

def normalize_expense(expense: Dict) -> Dict:
    normalized_expense = {
        "vendor": expense.get("vendor"),
        "date": expense.get("date"),
        "total": expense.get("total"),
        "items": expense.get("items")
    }
    return normalized_expense

def normalize_document_fields(fields: Dict) -> Dict:
    normalized_fields = {
        "merchant": fields.get("merchant"),
        "tax": fields.get("tax"),
        "total": fields.get("total"),
        "items": fields.get("items")
    }
    return normalized_fields