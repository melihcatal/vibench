"""
Query documents by a field value or partition-style key from a MongoDB Atlas managed NoSQL document store.
Uses the official PyMongo SDK (pymongo) for MongoDB Atlas integration.
"""

from typing import Any, Optional

from pymongo.collection import Collection

from database_client import get_collection
from database_models import (
    DocumentQueryRequest,
    DocumentListResponse,
    DocumentResponse,
    normalize_document_result,
)


def query_documents(
    collection_name: str,
    field_name: str,
    field_value: Any,
    limit: int = 100,
    client=None,
) -> DocumentListResponse:
    """
    Query documents from MongoDB Atlas that match a given field and value.

    Args:
        collection_name: Name of the MongoDB collection.
        field_name: Field to match against (can be a nested dotted path).
        field_value: Value to match.
        limit: Maximum number of documents to return.
        client: Optional pre-configured MongoClient instance.

    Returns:
        DocumentListResponse containing matched documents.
    """
    request = DocumentQueryRequest(
        collection_name=collection_name,
        field_name=field_name,
        field_value=field_value,
        limit=limit,
    )

    collection = get_collection(collection_name, client=client)

    try:
        query_filter = {field_name: field_value}
        cursor = collection.find(query_filter).limit(request.limit)
        raw_docs = list(cursor)

        documents = [normalize_document_result(doc) for doc in raw_docs]

        return DocumentListResponse(
            documents=documents,
            total_count=len(documents),
            error=None,
        )
    except Exception as exc:
        return DocumentListResponse(
            documents=[],
            total_count=0,
            error=str(exc),
        )


def query_by_partition_key(
    collection_name: str,
    partition_key: str,
    partition_value: Any,
    limit: int = 100,
    client=None,
) -> DocumentListResponse:
    """
    Convenience wrapper to query documents by a partition-style key in MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection.
        partition_key: The partition key field name (e.g., "tenant_id", "category").
        partition_value: The partition key value to filter on.
        limit: Maximum number of documents to return.
        client: Optional pre-configured MongoClient instance.

    Returns:
        DocumentListResponse containing matched documents.
    """
    return query_documents(
        collection_name=collection_name,
        field_name=partition_key,
        field_value=partition_value,
        limit=limit,
        client=client,
    )


if __name__ == "__main__":
    response = query_documents(
        collection_name="documents",
        field_name="category",
        field_value="sample",
    )
    print(response.to_dict())
