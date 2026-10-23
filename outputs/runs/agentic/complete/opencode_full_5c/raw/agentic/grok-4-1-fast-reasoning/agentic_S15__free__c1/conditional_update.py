import os
from datetime import datetime
from typing import Any, Dict
from database_client import get_mongo_client, get_database, get_documents_collection
from database_models import Document


def conditional_update(
    doc_id: str, updates: Dict[str, Any], expected_version: int
) -> bool:
    client = get_mongo_client()
    db = get_database(client)
    collection = get_documents_collection(db)
    now = datetime.utcnow().isoformat()
    result = collection.update_one(
        {"doc_id": doc_id, "version": expected_version},
        {"$set": {**updates, "version": expected_version + 1, "updated_at": now}},
    )
    return result.matched_count > 0
