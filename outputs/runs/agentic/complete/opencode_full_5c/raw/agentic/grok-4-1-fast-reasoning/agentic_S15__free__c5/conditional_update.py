from typing import Dict, Any
from datetime import datetime
from database_client import get_documents_collection


def conditional_update(
    doc_id: str, updates: Dict[str, Any], expected_version: int
) -> bool:
    collection = get_documents_collection()
    result = collection.find_one_and_update(
        {"doc_id": doc_id, "version": expected_version},
        {
            "$set": {**updates, "updated_at": datetime.utcnow().isoformat()},
            "$inc": {"version": 1},
        },
        return_document=True,
    )
    return result is not None
