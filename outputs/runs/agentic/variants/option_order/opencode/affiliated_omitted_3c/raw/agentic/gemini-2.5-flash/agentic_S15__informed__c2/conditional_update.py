import os
from typing import Any, Dict, Optional
from database_client import MongoDBClient
from database_models import DocumentUpdate


def conditional_update(update: DocumentUpdate) -> Dict[str, Any]:
    collection = MongoDBClient.get_collection()
    query = {"_id": update.id}
    if update.version is not None:
        query["version"] = update.version

    # Increment version for optimistic locking
    update_fields = {"$set": update.updates, "$inc": {"version": 1}}

    result = collection.update_one(query, update_fields)
    return {
        "id": update.id,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }
