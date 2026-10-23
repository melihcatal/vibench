from typing import Any, Dict, List, Optional

from database_client import get_collection
from database_models import DocumentResponse, QueryRequest, normalize_mongo_id


def query_documents(
    field: str,
    value: Any,
    partition_key: Optional[str] = None,
    limit: int = 100,
    sort_field: Optional[str] = None,
    sort_order: int = 1,
    projection: Optional[List[str]] = None,
    collection_name: Optional[str] = None,
    database_name: Optional[str] = None,
) -> DocumentResponse:
    request = QueryRequest(
        field=field,
        value=value,
        partition_key=partition_key,
        limit=limit,
        sort_field=sort_field,
        sort_order=sort_order,
        projection=projection,
    )

    collection = get_collection(collection_name, database_name)
    filter_query = request.to_mongo_filter()
    mongo_projection = request.to_mongo_projection()

    try:
        cursor = collection.find(filter_query, mongo_projection)

        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)

        cursor = cursor.limit(limit)

        documents = []
        for doc in cursor:
            documents.append(normalize_mongo_id(doc))

        return DocumentResponse(
            success=True,
            documents=documents,
            matched_count=len(documents),
        )
    except Exception as exc:
        return DocumentResponse(
            success=False,
            error=f"Query error: {exc}",
        )
