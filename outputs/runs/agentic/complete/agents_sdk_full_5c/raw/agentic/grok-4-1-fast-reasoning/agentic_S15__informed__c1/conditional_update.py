from typing import Dict, Any
from database_client import get_collection

def conditional_update(doc_id: str, updates: Dict[str, Any], expected_version: int) -> bool:
    result = get_collection().find_one_and_update(
        {"doc_id": doc_id, "version": expected_version},
        [
            {"$set": {**updates, "content": updates.get("content", {})}},  # adjust as needed
            {"$inc": {"version": 1}}
        ],
        return_document=True
    )
    return result is not None