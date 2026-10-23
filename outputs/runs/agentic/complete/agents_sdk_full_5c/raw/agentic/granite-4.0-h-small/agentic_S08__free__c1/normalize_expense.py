from typing import Dict, Any

def normalize_expense(expense: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema:
    {
        "vendor": str,
        "date": str,
        "total": float,
        "items": List[Dict[str, Any]]
    }
    """
    # Basic flattening and type coercion
    normalized = {
        "vendor": expense.get("vendor", "") or "Unknown Vendor",
        "date": str(expense.get("date", "")),
        "total": float(expense.get("total", 0)),
        "items": expense.get("items", [])
    }
    # Ensure items is a list of dicts
    if not isinstance(normalized["items"], list):
        normalized["items"] = []
    return normalized
