from typing import Dict, Any
from database_client import get_collection


def conditional_update(
    identifier: str, updates: Dict[str, Any], current_version: int
) -> bool:
    result = get_collection().update_one(
        {"_id": identifier, "version": current_version},
        {"$set": {**updates, "version": current_version + 1}},
    )
    return result.modified_count > 0
