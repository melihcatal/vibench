from database_client import get_collection
from database_models import QueryResponse, normalize_query_results


def query_documents(
    field_name: str,
    field_value: str,
    partition_key: str = "default",
    limit: int = 100,
) -> QueryResponse:
    collection = get_collection()

    query = {f"data.{field_name}": field_value}
    if partition_key:
        query["partition_key"] = partition_key

    cursor = collection.find(query).limit(limit)
    raw_docs = list(cursor)

    total_count = collection.count_documents(query)

    return normalize_query_results(raw_docs, total_count, partition_key)
