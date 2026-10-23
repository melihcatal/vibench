"""
Queries documents by a field value or partition-style key from MongoDB Atlas.

Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
Interface: SDK (pymongo)
"""

from typing import Any, Dict, List, Optional

from database_client import get_collection
from database_models import (
    format_query_filter,
    normalize_query_results,
    build_response,
)


def query_documents(
    partition_key: Optional[str] = None,
    field_name: Optional[str] = None,
    field_value: Optional[Any] = None,
    limit: int = 50,
    collection_name: Optional[str] = None,
    projection: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Query documents from MongoDB Atlas by partition key or field value.

    Args:
        partition_key: Partition key value to filter on.
        field_name: The field name to filter by.
        field_value: The field value to match.
        limit: Maximum number of documents to return.
        collection_name: Optional collection override.
        projection: Optional list of field names to include.

    Returns:
        A response dict with success status and list of matching documents.
    """
    collection = get_collection(collection_name)

    query_filter = format_query_filter(
        partition_key=partition_key,
        field_name=field_name,
        field_value=field_value,
    )

    if not query_filter:
        return build_response(
            success=False,
            error="MISSING_QUERY_PARAMS",
            message="At least one of partition_key or field_name/field_value must be provided.",
        )

    projection_dict = {field: 1 for field in projection} if projection else None

    cursor = collection.find(query_filter, projection=projection_dict).limit(limit)
    raw_results = list(cursor)

    results = normalize_query_results(raw_results, projection=projection)

    return build_response(
        success=True,
        data={
            "documents": results,
            "count": len(results),
            "limit": limit,
        },
        message=f"Queried {len(results)} document(s) from MongoDB Atlas.",
    )
