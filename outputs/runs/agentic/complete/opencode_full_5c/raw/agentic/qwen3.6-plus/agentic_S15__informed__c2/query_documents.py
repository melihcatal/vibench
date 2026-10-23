from __future__ import annotations

from typing import Any

from database_client import get_collection
from database_models import QueryResponse
from pymongo.collection import Collection


def query_documents(
    field: str,
    value: Any,
    partition_key: str | None = None,
    limit: int = 100,
    collection: Collection | None = None,
) -> QueryResponse:
    if collection is None:
        collection = get_collection()

    query_filter: dict[str, Any] = {f"data.{field}": value}

    if partition_key is not None:
        query_filter["partition_key"] = partition_key

    cursor = collection.find(query_filter).limit(limit)
    return QueryResponse.from_cursor(cursor, max_results=limit)
