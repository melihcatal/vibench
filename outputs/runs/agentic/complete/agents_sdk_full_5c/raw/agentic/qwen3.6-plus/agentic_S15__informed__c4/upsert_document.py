"""
Upserts a JSON document by its primary identifier in MongoDB Atlas.

Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
Interface: SDK (pymongo)
"""

from typing import Any, Dict, Optional

from database_client import get_collection
from database_models import prepare_upsert_payload, build_response


def upsert_document(
    document_id: str,
    data: Dict[str, Any],
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Upsert a document into MongoDB Atlas by its primary identifier.

    Uses pymongo's replace_one with upsert=True against a MongoDB Atlas cluster.

    Args:
        document_id: The primary identifier (_id) for the document.
        data: The document fields to upsert.
        collection_name: Optional collection override.

    Returns:
        A response dict with success status and matched/modified counts.
    """
    collection = get_collection(collection_name)
    payload = prepare_upsert_payload(document_id, data)

    result = collection.replace_one(
        {"_id": document_id},
        payload,
        upsert=True,
    )

    action = "inserted" if result.upserted_id is not None else "updated"

    return build_response(
        success=True,
        data={
            "document_id": document_id,
            "action": action,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None,
        },
        message=f"Document {action} successfully in MongoDB Atlas.",
    )
