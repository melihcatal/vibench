from database_client import get_collection
from database_models import (
    DocumentQueryRequest,
    QueryResponse,
    normalize_query_response,
)


def query_documents(request: DocumentQueryRequest) -> QueryResponse:
    collection = get_collection(request.collection)
    query_filter = {request.field_name: request.field_value}
    if request.partition_key:
        query_filter["partition_key"] = request.partition_key
    cursor = collection.find(query_filter).limit(request.limit)
    raw_docs = list(cursor)
    return normalize_query_response(raw_docs, request.collection)
