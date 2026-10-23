"""
Queries documents by a field value or partition-style key from MongoDB Atlas.
Uses the pymongo SDK to connect to MongoDB Atlas and perform filtered queries.
"""

from typing import Any, Dict, List, Optional

from database_client import create_client, normalize_document_for_read
from database_models import DocumentResponse, QueryResult, parse_raw_to_response


def query_documents(
    collection_name: str = "documents",
    partition_key: Optional[str] = None,
    field_name: Optional[str] = None,
    field_value: Any = None,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 100,
) -> QueryResult:
    """
    Query documents from MongoDB Atlas using field values or partition key.

    Args:
        collection_name: The MongoDB Atlas collection name.
        partition_key: Optional partition key to filter by.
        field_name: Optional field name to query by.
        field_value: Optional field value to match (used with field_name).
        filters: Optional dict of additional MongoDB query filters.
        limit: Maximum number of documents to return.

    Returns:
        QueryResult containing matching DocumentResponse objects.
    """
    client = create_client()
    try:
        collection = client.get_collection(collection_name)
        query_filter: Dict[str, Any] = {}

        if partition_key is not None:
            query_filter["partition_key"] = partition_key

        if field_name is not None and field_value is not None:
            query_filter[field_name] = field_value

        if filters is not None:
            query_filter.update(filters)

        cursor = collection.find(query_filter).limit(limit)
        documents: List[DocumentResponse] = []

        for raw_doc in cursor:
            doc_response = parse_raw_to_response(raw_doc)
            documents.append(doc_response)

        total_count = len(documents)
        return QueryResult(documents=documents, total_count=total_count)
    finally:
        client.close()


def query_documents_dict(
    collection_name: str = "documents",
    partition_key: Optional[str] = None,
    field_name: Optional[str] = None,
    field_value: Any = None,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    Convenience wrapper returning raw dict results instead of QueryResult.
    """
    result = query_documents(
        collection_name=collection_name,
        partition_key=partition_key,
        field_name=field_name,
        field_value=field_value,
        filters=filters,
        limit=limit,
    )
    return result.to_list()
