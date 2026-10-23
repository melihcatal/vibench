from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from document_client import get_mongodb_client


def store_expense_record(
    record: Dict[str, Any],
    database_name: str = "expenses",
    collection_name: str = "records",
) -> Dict[str, Any]:
    client = get_mongodb_client()
    collection = client[database_name][collection_name]
    payload = dict(record)
    payload.setdefault("stored_at", datetime.now(timezone.utc).isoformat())
    result = collection.insert_one(payload)
    return {
        "provider": "mongodb_atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }
