"""
Fetches a document by identifier from a MongoDB Atlas managed NoSQL store.

Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
Interface: SDK (pymongo)
"""

from typing import Any, Dict, List, Optional

from database_client import get_collection
from database_models import normalize_document, build_response


def fetch_document(
    document_id: str,
    collection_name: Optional[str] = None,
    projection: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Fetch a single document from MongoDB Atlas by its primary identifier.

    Args:
        document_id: The _id of the document to retrieve.
        collection_name: Optional collection override.
        projection: Optional list of field names to include in the response.

    Returns:
        A response dict with success status and the document data.
    """
    collection = get_collection(collection_name)

    projection_dict = {field: 1 for field in projection} if projection else None

    document = collection.find_one({"_id": document_id}, projection=projection_dict)

    if document is None:
        return build_response(
            success=False,
            message=f"Document with id '{document_id}' not found in MongoDB Atlas.",
            error="DOCUMENT_NOT_FOUND",
        )

    normalized = normalize_document(document)

    return build_response(
        success=True,
        data=normalized,
        message=f"Document fetched successfully from MongoDB Atlas.",
    )
