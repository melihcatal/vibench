from typing import Dict, Any

def normalize_expense(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    # Normalizes raw extraction results into a standard schema
    return {
        "vendor": raw_data.get("vendor"),
        "date": raw_data.get("date"),
        "total": raw_data.get("total"),
        "currency": "USD",  # Placeholder; real logic would detect currency
        "items": raw_data.get("line_items", []),
        "metadata": {}
    }
