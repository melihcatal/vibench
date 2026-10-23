"""
query_documents.py - Queries documents by a field value or partition-style key
in MongoDB Atlas. Uses the PyMongo SDK to run a find query against a managed
collection with optional filter criteria.
"""

from typing import Any, Dict, List, Optional

from database_client import build_atlas_client, AtlasClientHelper
from database_models import DocumentResponse, QueryResponse, normalize_mongo_object_id


def query_documents(
    collection_name: str,
    field_name: str,
    field_value: Any,
    limit: Optional[int] = 100,
    client: Optional[AtlasClientHelper] = None,
) -> QueryResponse:
    """
    Query documents from MongoDB Atlas where a given field matches a value.
    Supports partition-style queries by filtering on an indexed field.

    Args:
        collection_name: MongoDB collection to query.
        field_name: The field to filter on (supports nested fields with dot notation).
        field_value: The value to match.
        limit: Maximum number of documents to return.
        client: Optional pre-built AtlasClientHelper instance.

    Returns:
        QueryResponse containing matching DocumentResponse objects.
    """
    if client is None:
        client = build_atlas_client()

    collection = client.get_collection(collection_name)
    filter_query = {field_name: field_value}

    cursor = collection.find(filter_query).limit(limit if limit else 0)

    documents: List[DocumentResponse] = []
    count = 0
    has_more = False

    for raw_doc in cursor:
        if limit and count >= limit:
            has_more = True
            break
        raw_doc = normalize_mongo_object_id(raw_doc)
        documents.append(DocumentResponse.from_mongo_document(raw_doc))
        count += 1

    return QueryResponse(
        documents=documents,
        total_count=count,
        has_more=has_more,
    )


def query_documents_by_partition(
    collection_name: str,
    partition_key: str,
    partition_value: str,
    additional_filters: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = 100,
    client: Optional[AtlasClientHelper] = None,
) -> QueryResponse:
    """
    Query documents by a partition key (e.g. tenant_id, org_id) with optional
    additional filters, against MongoDB Atlas.

    Args:
        collection_name: MongoDB collection to query.
        partition_key: The field name used for partitioning (e.g. "tenant_id").
        partition_value: The partition value to match.
        additional_filters: Optional extra filter criteria merged into query.
        limit: Maximum number of documents to return.
        client: Optional pre-built AtlasClientHelper instance.

    Returns:
        QueryResponse with matching documents.
    """
    if client is None:
        client = build_atlas_client()

    collection = client.get_collection(collection_name)
    filter_query: Dict[str, Any] = {partition_key: partition_value}
    if additional_filters:
        filter_query.update(additional_filters)

    cursor = collection.find(filter_query).limit(limit if limit else 0)

    documents: List[DocumentResponse] = []
    count = 0
    has_more = False

    for raw_doc in cursor:
        if limit and count >= limit:
            has_more = True
            break
        raw_doc = normalize_mongo_object_id(raw_doc)
        documents.append(DocumentResponse.from_mongo_document(raw_doc))
        count += 1

    return QueryResponse(
        documents=documents,
        total_count=count,
        has_more=has_more,
    )


if __name__ == "__main__":
    resp = query_documents(
        collection_name="documents",
        field_name="metadata.source",
        field_value="upsert_document.py",
        limit=10,
    )
    print(resp.to_json())
