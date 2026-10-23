from typing import Any, Dict, List

from database_models import normalize_document


def summarize_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    normalized = [normalize_document(r) for r in records]
    return {
        "count": len(normalized),
        "document_ids": [r.get("document_id") for r in normalized],
        "latest_updated_at": max((r.get("updated_at", "") for r in normalized), default=""),
    }
