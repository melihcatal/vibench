"""
[SAME-SCENARIO] upsert_document.py
Upserts a JSON document by its primary identifier in MongoDB Atlas.
Provider: MongoDB Atlas via pymongo SDK.
Auth: MONGODB_ATLAS_URI
"""

import os
from typing import Any, Dict

from database_client import get_mongo_client, get_collection, get_database_name, get_collection_name
from database_models import DocumentRequest, DocumentResponse


def upsert_document(
    document_id: str,
    data: Dict[str, Any],
    partition_key: str | None = None,
    database_name: str | None = None,
    collection_name: str | None = None,
) -> DocumentResponse:
    """
    Upsert a document into the MongoDB Atlas collection by its primary identifier (_id).
    Uses MongoDB Atlas replace_one with upsert=True.

    Args:
        document_id: The primary identifier for the document.
        data: The JSON-serializable document payload.
        partition_key: Optional partition key for the document.
        database_name: Override for the target database name.
        collection_name: Override for the target collection name.

    Returns:
        DocumentResponse wrapping the upserted document.
    """
    client = get_mongo_client()
    try:
        db_name = database_name or get_database_name()
        col_name = collection_name or get_collection_name()
        collection = get_collection(client, db_name, col_name)

        request = DocumentRequest(
            document_id=document_id,
            data=data,
            partition_key=partition_key,
        )
        doc = request.to_mongo_doc()

        result = collection.replace_one(
            {"_id": document_id},
            doc,
            upsert=True,
        )

        if result.upserted_id:
            doc["_id"] = str(result.upserted_id)

        return DocumentResponse.from_mongo_doc(doc)
    finally:
        client.close()


if __name__ == "__main__":
    sample = upsert_document(
        document_id="doc-001",
        data={"title": "Sample Record", "body": "This is a test document."},
        partition_key="users",
    )
    print(f"Upserted: {sample.to_dict()}")
