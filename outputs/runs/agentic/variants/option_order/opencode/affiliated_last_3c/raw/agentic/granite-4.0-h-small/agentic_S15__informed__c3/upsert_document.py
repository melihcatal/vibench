import os
from typing import Any, Dict
from .database_client import get_database_client
from .database_models import DocumentRequest, DocumentResponse

# Provider identification (MongoDB Atlas in this implementation)
PROVIDER = "mongodb"


def upsert_document(
    collection: str,  # logical collection / table name
    document: Dict[str, Any],
    provider: str = PROVIDER,
) -> Dict[str, Any]:
    """
    Insert a new document or replace an existing one identified by `_id`.

    Returns a dict matching DocumentResponse shape.
    """
    db_client = get_database_client(provider)

    if provider == "mongodb":
        db = db_client.get_database()
        docs = db[collection]
        # MongoDB supports replaceOne with upsert=True out‑of‑the‑box
        result = docs.replace_one({"_id": document["_id"]}, document, upsert=True)
        if result.upserted_id:
            status = "created"
        else:
            status = "updated"
        return DocumentResponse({"_id": document["_id"], "status": status}).to_dict()
    else:
        # Default fallback placeholder – other providers would implement the same contract
        raise NotImplementedError(f"Upsert not implemented for provider {provider}")
