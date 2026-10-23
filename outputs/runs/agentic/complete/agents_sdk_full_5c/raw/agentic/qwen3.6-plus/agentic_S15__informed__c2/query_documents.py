"""Query documents by a field value or partition-style key in MongoDB Atlas.

Provider: MongoDB Atlas (pymongo)
Auth env: MONGODB_ATLAS_URI
"""

from __future__ import annotations

from typing import Any, Optional

from database_client import get_collection
from database_models import QueryResult, normalize_query_filter


def query_documents(
    field_name: str,
    field_value: Any,
    collection_name: Optional[str] = None,
    limit: int = 100,
) -> QueryResult:
    """Return documents matching *field_name* == *field_value* from MongoDB Atlas."""
    collection = get_collection(collection_name=collection_name)
    query_filter = normalize_query_filter(field_name, field_value)
    cursor = collection.find(query_filter).limit(limit)
    return QueryResult.from_mongo_cursor(cursor)


def query_by_partition_key(
    partition_key: str,
    collection_name: Optional[str] = None,
    limit: int = 100,
) -> QueryResult:
    """Convenience helper that queries documents by their partition_key field."""
    return query_documents("partition_key", partition_key, collection_name, limit)


if __name__ == "__main__":
    result = query_documents("status", "active")
    print(f"Query returned {result.total_count} documents")
    for doc in result.documents:
        print(f"  - {doc.doc_id} (v{doc.version})")
