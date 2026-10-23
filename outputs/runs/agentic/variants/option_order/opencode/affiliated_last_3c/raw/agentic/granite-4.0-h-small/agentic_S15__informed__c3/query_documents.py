import os
from typing import Any, Dict, List
from .database_client import get_database_client
from .database_models import DocumentRequest, DocumentResponse

# Provider identification (MongoDB Atlas in this implementation)
PROVIDER = "mongodb"


def query_documents(
    collection: str,
    filter: Dict[str, Any],
    provider: str = PROVIDER,
) -> Dict[str, Any]:
    """
    Query documents matching the provided filter criteria.

    Returns a dict matching DocumentResponse shape with a list of docs.
    """
    db_client = get_database_client(provider)

    if provider == "mongodb":
        db = db_client.get_database()
        docs = db[collection].find(filter)
        results = list(docs)
        return DocumentResponse({"results": results}).to_dict()
    else:
        raise NotImplementedError(f"Query not implemented for provider {provider}")
