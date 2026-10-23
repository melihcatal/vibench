from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ExpenseItem:
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None


def field_text(fields: List[Dict[str, Any]], field_type: str, default: str = "") -> str:
    for field in fields:
        if field.get("Type", {}).get("Text") == field_type:
            return field.get("ValueDetection", {}).get("Text", default)
    return default


def normalize_expense_schema(expense: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": expense.get("vendor", ""),
        "date": expense.get("date", ""),
        "total": expense.get("total", ""),
        "tax": expense.get("tax", ""),
        "items": expense.get("items", []),
    }
