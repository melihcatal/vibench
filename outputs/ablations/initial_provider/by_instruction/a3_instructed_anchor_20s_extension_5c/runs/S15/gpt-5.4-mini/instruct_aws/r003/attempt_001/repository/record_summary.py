from typing import Any, Dict

from database_models import normalize_document


def record_summary(record: Dict[str, Any]) -> Dict[str, Any]:
    data = normalize_document(record)
    return {
        "id": data.get("id"),
        "title": data.get("title") or data.get("name"),
        "field_count": len(data),
    }
