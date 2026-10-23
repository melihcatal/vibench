import os
from typing import Any, Dict
from .database_client import get_database_client
from .database_models import DocumentRequest, DocumentResponse

# Provider identification (MongoDB Atlas in this implementation)
PROVIDER = "mongodb"


def fetch_document(
    collection: str,
    doc_id: str,
    provider: str = PROVIDER,
) -> Dict[str, Any]:
    """
    Retrieve a single document by its primary identifier `_id`.

    Returns a dict matching DocumentResponse shape.
    """
    db_client = get_database_client(provider)

    if provider == "mongodb":
        db = db_client.get_database()
        docs = db[collection]
        result = docs.find_one({"_id": doc_id})
        if not result:
            return DocumentResponse({"error": "not found"}, status="error").to_dict()
        # Omit _id if you prefer a plain payload
        return DocumentResponse(result).to_dict()
    else:
        raise NotImplementedError(f"Fetch not implemented for provider {provider}")
