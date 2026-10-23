"""
Queries documents by a field value or partition-style key in MongoDB Atlas.
Uses pymongo for MongoDB Atlas managed NoSQL document store integration.
"""

from __future__ import annotations

from typing import Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from database_client import get_collection, create_mongo_client
from database_models import QueryFilter, QueryResponse, DocumentRecord, sanitize_for_mongo


def query_documents(
    field_name: str,
    field_value: Any,
    partition_key: Optional[str] = None,
    exact_match: bool = True,
    limit: Optional[int] = None,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> QueryResponse:
    """
    Query documents from MongoDB Atlas by a field value and optional partition key.
    
    Args:
        field_name: The field within the document 'data' to query against.
        field_value: The value to match.
        partition_key: Optional partition key for scoped queries.
        exact_match: Whether to perform exact matching or regex matching.
        limit: Optional maximum number of documents to return.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A QueryResponse containing matched documents and metadata.
    """
    if collection is None:
        collection = get_collection(client)

    query = QueryFilter(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        exact_match=exact_match,
    )

    mongo_filter = query.to_mongo_filter()
    cursor: Cursor = collection.find(mongo_filter)

    if limit is not None:
        cursor = cursor.limit(limit)

    documents = []
    total_count = 0
    for raw_doc in cursor:
        record = DocumentRecord.from_mongo_document(raw_doc)
        documents.append(record)
        total_count += 1

    return QueryResponse(documents=documents, total_count=total_count)


def query_documents_by_partition(
    partition_key: str,
    additional_filters: Optional[dict[str, Any]] = None,
    limit: Optional[int] = None,
    sort_field: Optional[str] = None,
    sort_order: int = -1,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> QueryResponse:
    """
    Query documents from MongoDB Atlas scoped to a specific partition key.
    
    This is useful for tenant-scoped or namespace-scoped document retrieval.
    
    Args:
        partition_key: The partition key value to filter by.
        additional_filters: Optional additional field-based filters on the document data.
        limit: Optional maximum number of documents to return.
        sort_field: Optional field within 'data' to sort by.
        sort_order: Sort direction (-1 for descending, 1 for ascending).
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A QueryResponse containing matched documents and metadata.
    """
    if collection is None:
        collection = get_collection(client)

    mongo_filter: dict[str, Any] = {"partition_key": partition_key}
    if additional_filters:
        for fname, fval in additional_filters.items():
            mongo_filter[f"data.{fname}"] = sanitize_for_mongo(fval)

    cursor: Cursor = collection.find(mongo_filter)

    if sort_field:
        cursor = cursor.sort(f"data.{sort_field}", sort_order)

    if limit is not None:
        cursor = cursor.limit(limit)

    documents = []
    total_count = 0
    for raw_doc in cursor:
        record = DocumentRecord.from_mongo_document(raw_doc)
        documents.append(record)
        total_count += 1

    return QueryResponse(documents=documents, total_count=total_count)


def query_documents_with_full_text(
    search_term: str,
    partition_key: Optional[str] = None,
    limit: int = 20,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> QueryResponse:
    """
    Query documents from MongoDB Atlas using a text search on indexed fields.
    
    Requires a text index to be created on the MongoDB Atlas collection, e.g.:
    collection.create_index([("data.$**", "text")])
    
    Args:
        search_term: The text search term.
        partition_key: Optional partition key for scoped queries.
        limit: Maximum number of documents to return.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A QueryResponse containing matched documents and metadata.
    """
    if collection is None:
        collection = get_collection(client)

    mongo_filter: dict[str, Any] = {"$text": {"$search": search_term}}
    if partition_key:
        mongo_filter["partition_key"] = partition_key

    cursor = collection.find(mongo_filter, {"score": {"$meta": "textScore"}}).limit(limit)

    documents = []
    total_count = 0
    for raw_doc in cursor:
        record = DocumentRecord.from_mongo_document(raw_doc)
        documents.append(record)
        total_count += 1

    return QueryResponse(documents=documents, total_count=total_count)


if __name__ == "__main__":
    client = create_mongo_client()
    try:
        response = query_documents(
            field_name="status",
            field_value="active",
            client=client,
        )
        print(response.to_dict())
    finally:
        client.close()
