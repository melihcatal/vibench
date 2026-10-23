"""
[SAME-SCENARIO] query_documents.py
Queries documents by a field value or partition-style key from MongoDB Atlas.
Provider: MongoDB Atlas via pymongo SDK.
Auth: MONGODB_ATLAS_URI
"""

from typing import Any, Dict, List, Optional

from database_client import get_mongo_client, get_collection, get_database_name, get_collection_name
from database_models import DocumentResponse, QueryResult


def query_documents(
    field_name: str,
    field_value: Any,
    limit: int = 100,
    database_name: str | None = None,
    collection_name: str | None = None,
) -> QueryResult:
    """
    Query MongoDB Atlas for documents matching a given field value.
    Supports partition-key style queries as well as arbitrary field matching.

    Args:
        field_name: The document field to filter on (e.g., 'partition_key', 'data.category').
        field_value: The value to match.
        limit: Maximum number of documents to return.
        database_name: Optional override for the target database name.
        collection_name: Optional override for the target collection name.

    Returns:
        QueryResult containing matched DocumentResponse objects and a total count.
    """
    client = get_mongo_client()
    try:
        db_name = database_name or get_database_name()
        col_name = collection_name or get_collection_name()
        collection = get_collection(client, db_name, col_name)

        query_filter = {field_name: field_value}

        cursor = collection.find(query_filter).limit(limit)
        raw_docs = list(cursor)

        count = collection.count_documents(query_filter)

        documents = [DocumentResponse.from_mongo_doc(doc) for doc in raw_docs]

        return QueryResult(documents=documents, total_count=count)
    finally:
        client.close()


if __name__ == "__main__":
    results = query_documents("partition_key", "users")
    print(f"Found {results.total_count} documents.")
    for doc in results.documents:
        print(f"  - {doc.document_id}: {doc.data}")
