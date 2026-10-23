"""
[SAME-SCENARIO] fetch_document.py
Fetches a document by identifier from MongoDB Atlas managed NoSQL store.
Provider: MongoDB Atlas via pymongo SDK.
Auth: MONGODB_ATLAS_URI
"""

from typing import Optional

from database_client import get_mongo_client, get_collection, get_database_name, get_collection_name
from database_models import DocumentResponse


def fetch_document(
    document_id: str,
    database_name: str | None = None,
    collection_name: str | None = None,
) -> Optional[DocumentResponse]:
    """
    Retrieve a single document from MongoDB Atlas by its _id.

    Args:
        document_id: The primary identifier of the document to fetch.
        database_name: Optional override for the target database name.
        collection_name: Optional override for the target collection name.

    Returns:
        DocumentResponse if found, otherwise None.
    """
    client = get_mongo_client()
    try:
        db_name = database_name or get_database_name()
        col_name = collection_name or get_collection_name()
        collection = get_collection(client, db_name, col_name)

        raw_doc = collection.find_one({"_id": document_id})
        if raw_doc is None:
            return None

        return DocumentResponse.from_mongo_doc(raw_doc)
    finally:
        client.close()


if __name__ == "__main__":
    result = fetch_document("doc-001")
    if result:
        print(f"Fetched: {result.to_dict()}")
    else:
        print("Document not found.")
