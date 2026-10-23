import os
from typing import Dict, Any, Optional
from database_client import get_database_client, get_database, get_collection
from pymongo.errors import PyMongoError


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    expected_version: int,
    db_name: str = "document_store_db",
    collection_name: str = "documents",
):
    client = get_database_client()
    db = get_database(client, db_name)
    collection = get_collection(db, collection_name)

    try:
        # MongoDB Atlas (pymongo) for conditional updates using a version field.
        # The update_one method is part of the pymongo.collection.Collection class.
        # We use $set for updates and $inc to increment the version.
        result = collection.update_one(
            {"_id": document_id, "version": expected_version},
            {
                "$set": {f"content.{k}": v for k, v in updates.items()},
                "$inc": {"version": 1},
            },
        )
        client.close()
        if result.matched_count == 0:
            # If no document was matched, it means the version did not match or the document does not exist.
            existing_doc = collection.find_one({"_id": document_id})
            if existing_doc:
                return {
                    "success": False,
                    "message": f"Version mismatch. Expected {expected_version}, but found {existing_doc.get('version')}",
                }
            else:
                return {"success": False, "message": "Document not found"}
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
        }
    except PyMongoError as e:
        client.close()
        return {"success": False, "message": str(e)}
