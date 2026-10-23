import os
from typing import Any, Dict
from database_client import MongoDBClient
from database_models import Document


def upsert_document(document: Document) -> Dict[str, Any]:
    collection = MongoDBClient.get_collection()
    result = collection.update_one(
        {"_id": document.id}, {"$set": document.content}, upsert=True
    )
    return {
        "id": document.id,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }
